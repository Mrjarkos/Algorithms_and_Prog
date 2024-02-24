from Objects.Administrativo import Administrativo
from Objects.Estudiante import Estudiante
from Objects.Profesor import Profesor


USER_TYPE_LIST = [cl.__name__ for cl in [Administrativo, Estudiante, Profesor]]
USER_TYPE_DICT = {
    Administrativo.__name__ : Administrativo,
    Estudiante.__name__ : Estudiante,
    Profesor.__name__ : Profesor
}
