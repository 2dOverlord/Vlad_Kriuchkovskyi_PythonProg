from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits


class Memento(ABC):
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass


class ConcreteMemento(Memento):
    def __init__(self, collection, file_name=None):
        self.collection = collection
        if file_name:
            with open(file_name, 'r') as file:
                file.seek(0, 0)
                file_text = file.read()
            self.file_info = {
                'name': file_name,
                'text': file_text
            }
        else:
            self.file_info = None
        self._date = str(datetime.now())[:19]

    def get_state(self) -> str:
        """
        The Originator uses this method when restoring its state.
        """
        return self.collection[:], self.file_info

    def get_name(self) -> str:
        """
        The rest of the methods are used by the Caretaker to display metadata.
        """

        return f"{self._date} / ({str(self.collection)}...)"

    def get_date(self) -> str:
        return self._date


class Caretaker:
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """

    def __init__(self, originator) -> None:
        self._mementos = []
        self.id = -1
        self._originator = originator

    def backup(self) -> None:
        print("\nCaretaker: Saving Originator's state...")
        if len(self._mementos) == self.id + 1:
            self._mementos.append(self._originator.save())
        else:
            self._mementos[self.id + 1] = self._originator.save()
        self.id += 1

    def undo(self) -> None:
        if not len(self._mementos) or self.id == 0:
            return

        self.id -= 1
        memento = self._mementos[self.id]
        print(f"Caretaker: Restoring state to: {memento.get_name()}")
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    def redo(self):
        if not len(self._mementos) or self.id == len(self._mementos):
            return

        self.id += 1
        memento = self._mementos[self.id]

        print(f"Caretaker: Restoring state to: {memento.get_name()}")
        try:
            self._originator.restore(memento)
        except Exception:
            self.redo()

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento.get_name())

#
# if __name__ == "__main__":
#     originator = Originator("Super-duper-super-puper-super.")
#     caretaker = Caretaker(originator)
#
#     caretaker.backup()
#     originator.do_something()
#
#     caretaker.backup()
#     originator.do_something()
#
#     caretaker.backup()
#     originator.do_something()
#
#     print()
#     caretaker.show_history()
#
#     print("\nClient: Now, let's rollback!\n")
#     caretaker.undo()
#
#     print("\nClient: Once more!\n")
#     caretaker.undo()
