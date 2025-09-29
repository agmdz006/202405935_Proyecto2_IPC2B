class DiccionarioPersonalizado:
    """
    Implementación personalizada de un diccionario usando una lista enlazada
    para almacenar pares clave-valor.
    """
    
    def __init__(self):
        """Inicializa un diccionario vacío."""
        from .lista_enlazada import ListaEnlazada
        self.pares = ListaEnlazada()
    
    def insertar(self, clave, valor):
        """
        Inserta o actualiza un par clave-valor en el diccionario.
        
        Args:
            clave: La clave del elemento
            valor: El valor asociado a la clave
        """
        # Buscar si la clave ya existe
        actual = self.pares.cabeza
        while actual:
            if actual.dato['clave'] == clave:
                actual.dato['valor'] = valor
                return
            actual = actual.siguiente
        
        # Si no existe, agregar nuevo par
        par = {'clave': clave, 'valor': valor}
        self.pares.agregar(par)
    
    def buscar(self, clave, valor_por_defecto=None):
        """
        Busca un valor por su clave.
        
        Args:
            clave: La clave a buscar
            valor_por_defecto: Valor a retornar si no se encuentra la clave
            
        Returns:
            El valor asociado a la clave o valor_por_defecto si no existe
        """
        actual = self.pares.cabeza
        while actual:
            if actual.dato['clave'] == clave:
                return actual.dato['valor']
            actual = actual.siguiente
        return valor_por_defecto
    
    def contiene(self, clave):
        """
        Verifica si una clave existe en el diccionario.
        
        Args:
            clave: La clave a verificar
            
        Returns:
            True si la clave existe, False en caso contrario
        """
        actual = self.pares.cabeza
        while actual:
            if actual.dato['clave'] == clave:
                return True
            actual = actual.siguiente
        return False
    
    def eliminar(self, clave):
        """
        Elimina un par clave-valor del diccionario.
        
        Args:
            clave: La clave del elemento a eliminar
            
        Returns:
            True si se eliminó, False si no se encontró
        """
        actual = self.pares.cabeza
        anterior = None
        
        while actual:
            if actual.dato['clave'] == clave:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.pares.cabeza = actual.siguiente
                self.pares.tamaño -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False
    
    def obtener_claves(self):
        """
        Obtiene todas las claves del diccionario.
        
        Returns:
            ListaEnlazada con todas las claves
        """
        from .lista_enlazada import ListaEnlazada
        claves = ListaEnlazada()
        actual = self.pares.cabeza
        while actual:
            claves.agregar(actual.dato['clave'])
            actual = actual.siguiente
        return claves
    
    def obtener_valores(self):
        """
        Obtiene todos los valores del diccionario.
        
        Returns:
            ListaEnlazada con todos los valores
        """
        from .lista_enlazada import ListaEnlazada
        valores = ListaEnlazada()
        actual = self.pares.cabeza
        while actual:
            valores.agregar(actual.dato['valor'])
            actual = actual.siguiente
        return valores
    
    def esta_vacio(self):
        """
        Verifica si el diccionario está vacío.
        
        Returns:
            True si está vacío, False en caso contrario
        """
        return self.pares.esta_vacia()
    
    def tamaño(self):
        """
        Obtiene el número de elementos en el diccionario.
        
        Returns:
            Número de pares clave-valor
        """
        return self.pares.tamaño
