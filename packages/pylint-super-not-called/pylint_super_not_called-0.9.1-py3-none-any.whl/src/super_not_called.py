from typing import TYPE_CHECKING

import astroid
from astroid import bases, nodes
from pylint.checkers import BaseChecker, utils
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import decorated_with, is_builtin_object, node_frame_class
from pylint.interfaces import INFERENCE

if TYPE_CHECKING:
    from pylint.lint import PyLinter



def register(linter: 'PyLinter') -> None:
    """
    This required method auto registers the checker during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(SuperNotCalledChecker(linter))


def _ancestors_to_call(klass_node: nodes.ClassDef, method='__init__') -> dict[nodes.ClassDef, bases.UnboundMethod]:
    """
    Return a dictionary where keys are the list of base classes providing
    the queried method, and so that should/may be called from the method node.
    """
    to_call: dict[nodes.ClassDef, bases.UnboundMethod] = {}
    for base_node in klass_node.ancestors(recurs=False):
        try:
            to_call[base_node] = next(base_node.igetattr(method))
        except astroid.InferenceError:
            continue
    return to_call


class SuperNotCalledChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = 'super-not-called'
    priority = -1
    msgs = {
        'E6751': (
            'Super method from base class %r is not called',
            'super-not-called',
            'Used when an ancestor class method has an overloaded method which is not called by a derived class.',
        ),
    }
    options = (
        (
            'super-enforced-methods',
            {
                "default": ('setUp',),
                "type": 'csv',
                'metavar': '<method names>',
                'help': 'List of overloaded method to check for parent method call with super()',
            },
        ),
    )

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Check method arguments, overriding."""
        if not node.is_method():
            return
        if not self.linter.is_message_enabled('super-not-called'):
            return
        methods_to_check = self.linter.config.super_enforced_methods
        if node.name in methods_to_check:
            klass: 'nodes.ClassDef' = node.parent.frame(future=True)
            self._check_method_called(node, klass, node.name)

    def _check_method_called(self, node: nodes.FunctionDef, klass_node: nodes.ClassDef, method_name: str) -> None:
        """
        Check that the method call super or ancestors'method (unless it is used for type hinting with `typing.overload`).
        """
        to_call = None
        for stmt in node.nodes_of_class(nodes.Call):
            expr = stmt.func
            if not isinstance(expr, nodes.Attribute) or expr.attrname != method_name:
                continue

            to_call = _ancestors_to_call(klass_node, expr.attrname)

            # skip the test if using super
            if isinstance(expr.expr, nodes.Call) and isinstance(expr.expr.func, nodes.Name) and expr.expr.func.name == 'super':
                return
            try:
                for klass in expr.expr.infer():
                    if klass is astroid.Uninferable:
                        continue

                    # The inferred klass can be super(), which was
                    # assigned to a variable and the method
                    # was called later.
                    #
                    # base = super()
                    # base.__init__(...)

                    if (
                        isinstance(klass, astroid.Instance)
                        and isinstance(klass._proxied, nodes.ClassDef)
                        and is_builtin_object(klass._proxied)
                        and klass._proxied.name == 'super'
                    ):
                        return
                    if isinstance(klass, astroid.objects.Super):
                        return
            except astroid.InferenceError:
                continue
        if to_call:
            for klass, method in dict(to_call).items():
                # Return if klass is protocol
                if klass.qname() in utils.TYPING_PROTOCOLS:
                    return

                # Return if any of the klass' first-order bases is protocol
                for base in klass.bases:
                    try:
                        for inf_base in base.infer():
                            if inf_base.qname() in utils.TYPING_PROTOCOLS:
                                return
                    except astroid.InferenceError:
                        continue

                if decorated_with(node, ['typing.overload']):
                    continue
                cls = node_frame_class(method)
                if klass.name == 'object' or (cls and cls.name == 'object'):
                    continue
        self.add_message(
            'super-not-called',
            args=method_name,
            node=node,
            confidence=INFERENCE,
        )
