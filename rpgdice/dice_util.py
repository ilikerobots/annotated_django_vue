from typing import Any

import d20
from d20 import Die, SimpleStringifier


def roll_dice(dice_notation: object) -> tuple[int, list[dict[str, int]], str]:
    roll = d20.roll(dice_notation, stringifier=DiceHTMLStringifier())
    dice_results = _extract_dice_results(roll.expr)
    return roll.total, [{'size': d.size, 'value': d.total} for d in dice_results], str(roll)

def _extract_dice_results(roll_result: object) -> list[Any]:
    dice_results = []

    def _traverse_node(node: object) -> None:
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                _traverse_node(child)
        elif hasattr(node, 'values'):
            dice_results.extend(v for v in node.values if isinstance(v, Die))

    _traverse_node(roll_result)

    return dice_results


class DiceHTMLStringifier(SimpleStringifier):
    def _str_expression(self, node: object) -> str:
        return f'<span class="dice-expression">{self._stringify(node.roll)}</span>'

    def _str_dice(self, node: object) -> str:
        dice_icons = [
            f'<dice-icon size="{die.size}" value="{value.values[0]}"></dice-icon>'
            for die in node.values
            for value in die.values
        ]
        return ''.join(dice_icons)
        # the_dice = [self._stringify(die) for die in node.values]
        # return f'<span class="dice-set">[{', '.join(the_dice)}]</span>'

    def _str_literal(self, node: object) -> str:
        return f'<span class="dice-literal">{node.values[0]}</span>'

    def _str_parenthetical(self, node: object) -> str:
        return f'<span class="dice-parenthetical">({self._stringify(node.expr)})</span>'

    def _str_unary_op(self, node: object) -> str:
        return f'<span class="dice-unary-op">{node.op}</span>{self._stringify(node.expr)}'

    def _str_binary_op(self, node: object) -> str:
        return f'{self._stringify(node.left)} <span class="dice-binary-op">{node.op}</span> {self._stringify(node.right)}'

