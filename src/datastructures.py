
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
        # example list of members
        # Generamos los objetos con cada miembro de la familia y sus características
        self._members = [{
            "id": self._generateId(),
            "first_name": "John",
            "last_name": last_name,
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        }, 
        {
            "id": self._generateId(),
            "first_name": "Jane",
            "last_name": last_name,
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        },
        {
            "id": self._generateId(),
            "first_name": "Jimmy",
            "last_name": last_name,
            "age": 5,
            "lucky_numbers": [1]
        }]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, new_member):
        # Estamos fijando que last name sea el mismo para todos los miembros
        new_member["last_name"] = self.last_name
        # Lo añadimos al array de miembros
        self._members.append(new_member)
        # Devolvemos el miembro nuevo
        return new_member

        pass

    def delete_member(self, id):

        for member in self._members:
          if member["id"] == id :
              self._members.remove(member)
              return member
          else :
              member_id_not_found = {}
              return member_id_not_found
          
        # Hacemos un for para buscar el id que queramos eliminar, comparamos los id y si coincide, elimina el member con ese 
        #   del array de members y retornamos el member a eliminar en la funcion del app.

    def get_member(self, id):
        # print(id)
        # La función recorre self.members y por cada miembro busca si el id es igual al id del la ruta del enlace, si coincide 
        # mostrar el miembro de la familia con el id que coincide. Le pasamos el parametro a app.py en la ruta member/id
        for one_member in self._members:
          if one_member["id"] == id :
              return one_member
          else :
            member_id_not_found = {}
            return member_id_not_found
          

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
