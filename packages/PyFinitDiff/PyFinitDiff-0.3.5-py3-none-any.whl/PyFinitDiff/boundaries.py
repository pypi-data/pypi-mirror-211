#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass()
class Boundaries2D():
    left: str = 'zero'
    """ Value of the left boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    right: str = 'zero'
    """ Value of the right boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    top: str = 'zero'
    """ Value of the top boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    bottom: str = 'zero'
    """ Value of the bottom boundary, either ['zero', 'symmetric', 'anti-symmetric'] """

    acceptable_boundary = ['zero', 'symmetric', 'anti-symmetric']
    all_boundaries = ['left', 'right', 'top', 'bottom']

    def __post_init__(self):
        for boundary in self.all_boundaries:
            self.assert_boundary_acceptable(boundary_string=boundary)

        self.assert_both_boundaries_not_same(self.left, self.right)
        self.assert_both_boundaries_not_same(self.top, self.bottom)

    def assert_boundary_acceptable(self, boundary_string: str) -> None:
        boundary = getattr(self, boundary_string)
        if boundary not in self.acceptable_boundary:
            raise ValueError(f"Error: {boundary_string} boundary: {boundary} argument not accepted. {self.acceptable_boundary}")

    @property
    def dictionary(self):
        return {
            'left': self.left,
            'right': self.right,
            'top': self.top,
            'bottom': self.bottom
        }

    @property
    def x_symmetry(self):
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    @property
    def y_symmetry(self):
        if self.top == 'symmetric' or self.bottom == 'symmetric':
            return 'symmetric'
        elif self.top == 'anti-symmetric' or self.bottom == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str):
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Both left and right or top and "
                              "bottom symmetry shouldn't be the same "
                              "if symmetric or anti-symmetric")


@dataclass()
class Boundaries1D():
    left: str = 'zero'
    """ Value of the left boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    right: str = 'zero'
    """ Value of the right boundary, either ['zero', 'symmetric', 'anti-symmetric'] """

    def __post_init__(self):
        self.assert_both_boundaries_not_same(self.left, self.right)

    @property
    def dictionary(self):
        return {
            'left': self.left,
            'right': self.right
        }

    @property
    def x_symmetry(self):
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str):
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Both left and right or top and "
                              "bottom symmetry shouldn't be the same "
                              "if symmetric or anti-symmetric")