
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = [
                {"id":1,
                "name":"John",
                "last_name":"Jackson",
                "age":33,
                "lucky_numbers": [7, 13, 22]},

                {"id":2,
                "name":"Jane",
                "last_name":"Jackson",
                "age":35,
                "lucky_numbers": [10, 14, 3]},

                {"id":3,
                "name":"Jimmy ",
                "last_name":"Jackson",
                "age":5,
                "lucky_numbers": [1]}
            ]

    # Este método genera un 'id' único al agregar miembros a la lista (no debes modificar esta función)
    def _generate_id(self):
        return randint(0, 99999999)

    def add_member(self, member):
       member["id"]=self._generate_id()
       member["last_name"]=self.last_name
       self._members.append(member)
       return f"añadido {member}"
        ## Debes implementar este método
        ## Agrega un nuevo miembro a la lista de _members
        

    def delete_member(self, id):
        for member in self._members:
            if member["id"]==id:
                self._members.remove(member)
        return f"Usuario con el id {id} Eliminado"

    def get_member(self, id):
         for member in self._members:
            if member["id"]==id:
                return member
    def get_all_members(self):
        return self._members

