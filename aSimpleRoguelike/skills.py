class BaseSkill():
    def __init__(self,name):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return f'Skill<{self.name}>'
MoveUp = BaseSkill("MoveUp")
MoveDown = BaseSkill("MoveDown")
MoveLeft = BaseSkill("MoveLeft")
MoveRight = BaseSkill("MoveRight")

Conflicts = [
    [MoveUp,MoveDown],
    [MoveLeft,MoveRight],
]