import inspect
import random
from datetime import timedelta, datetime
from typing import Type

from seleniumbot.core.action import Action, AFKAction, ActionException
from seleniumbot.core.client import SeleniumClient
from seleniumbot.utils import get_logger
from seleniumbot.utils.randomizer import Randomizer

logger = get_logger(__name__)


class SeleniumBot:
    def __init__(self, start_action: Type[Action] | Action, work_time: timedelta, **kwargs):
        self.start_time = datetime.now()
        self.end_time = self.start_time + work_time

        options = kwargs.get('options')
        seleniumwire_options = kwargs.get('seleniumwire_options')
        self.client = SeleniumClient(options=options, seleniumwire_options=seleniumwire_options)

        self.navigations = []
        self.actions: list[Action] = []
        self.last_action: Action | None = None

        if inspect.isclass(start_action):
            start_action = start_action()

        start_action.execute(self.client, self.last_action)

        self.history = set()

        self.__comp = lambda action, x: action.coefficient > x

    def set_navigation_actions(self, actions: list[Type[Action]]):
        self.navigations = [action() for action in actions]

    def start(self) -> None:
        while True:
            if datetime.now() > self.end_time:
                logger.info('Work time ended, going home. Bye.')
                break

            try:
                self._run_action()
            except ActionException as e:
                logger.error(f'ActionException raised - {e}')
                break

    def _run_action(self) -> None:
        if not self.actions:
            action = Randomizer.random_item_from_list(items=self.navigations, comp=self.__comp, default=AFKAction())
            new_actions = action.execute(self.client, self.last_action)
            self.__set_actions(new_actions)
        else:
            action = Randomizer.random_item_from_list(items=self.actions, comp=self.__comp, default=AFKAction())
            action.execute(self.client, self.last_action)

            # If random actions is AFKAction, then we can't delete it, since it wasn't in our `self.actions`
            if not isinstance(action, AFKAction):
                self.actions.remove(action)

            if action.flush_actions:
                self.actions = []

        self.last_action = action

    def __set_actions(self, new_actions: list[Action]) -> None:
        random.shuffle(new_actions)
        new_actions = new_actions[:int(len(new_actions) / 2)]
        self.actions = new_actions
