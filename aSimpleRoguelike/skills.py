class BaseSkill():
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'Skill<{self.name}>'

    def load(self, actor):
        raise NotImplementedError

    def cast(self, actor):
        raise NotImplementedError


class MoveUp(BaseSkill):
    name = "MoveUp"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_v = 0
        actor.speed_v = actor.MAX_SPEED


class MoveDown(BaseSkill):
    name = "MoveDown"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_v = 0
        actor.speed_v = -actor.MAX_SPEED


class MoveLeft(BaseSkill):
    name = "MoveLeft"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_h = 0
        actor.speed_h = -actor.MAX_SPEED


class MoveRight(BaseSkill):
    name = "MoveRight"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_h = 0
        actor.speed_h = actor.MAX_SPEED


class MoveUpEnd(BaseSkill):
    name = "MoveUpEnd"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_v = 0


class MoveDownEnd(BaseSkill):
    name = "MoveDownEnd"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_v = 0


class MoveLeftEnd(BaseSkill):
    name = "MoveLeftEnd"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_h = 0


class MoveRightEnd(BaseSkill):
    name = "MoveRightEnd"
    load_only = True

    @classmethod
    def load(cls, actor):
        actor.speed_h = 0
