from order_with_respect_to.base_tests import BaseOrderWithRespectToTests

from paradoxdjango.test import TestCase

from .models import Answer, Post, Question


class OrderWithRespectToGFKTests(BaseOrderWithRespectToTests, TestCase):
    Answer = Answer
    Post = Post
    Question = Question
