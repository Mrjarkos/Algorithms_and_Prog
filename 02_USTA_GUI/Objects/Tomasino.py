class Tomasino(object):
    #cod : int = 0
    cod : int 
    first_name : str
    last_name : str
    id : int
    email : str
    _password : str
    
    # def __new__(cls, first_name, last_name, id, cod, email, password, obj=None):
    #     # Custom logic before creating the instance
    #     print("Creating a new instance of MyCustomClass...")
    #     instance = super().__new__(cls)
    #     if obj is not None:
    #         instance.first_name = obj.first_name
    #         instance.last_name = obj.last_name
    #         instance.id = obj.id,
    #         instance.cod = obj.cod
    #         instance.email = obj.email
    #         instance._password = obj._password
        
    #     return instance
         
    def __init__(self, first_name, last_name, id, cod, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id 
        # self.cod = Tomasino.cod = Tomasino.cod +1
        self.cod = cod
        self.email = email
        self._password = password
    
    def update_password(self, old_pssw, new_pssw):
        if old_pssw != self._password:
            err_msg = "ExpectedValueException: Las contraseñas no coinciden. No es posible actualizar"
            return err_msg
        self._password = new_pssw
    
    def as_list(self):
        # Include only public fields
        fields_to_include = [str(p) for p in Tomasino.__annotations__ if not p.startswith("_")]
        return [getattr(self, f) for f in fields_to_include]

    def as_str_list(self):
        fields_to_include = [str(p) for p in Tomasino.__annotations__ if not p.startswith("_")]
        return [str(getattr(self, f)) for f in fields_to_include]
    
    def get_attribute_from_format(self, format_attr):
        return {
            "Codigo": self.cod,
            "Nombre": self.first_name,
            "Apellido": self.last_name,
            "Identificacion": self.id,
            "Email": self._password
        }[format_attr]
        
    @staticmethod
    def get_public_format_properties():
        return [
            "Codigo",
            "Nombre",
            "Apellido",
            "Identificacion",
            "Email"
        ]
        
    
    