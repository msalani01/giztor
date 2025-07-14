import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog
)
from PyQt5.QtGui import QColor

class GestorProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛒 Gestor de Productos V2")
        self.setGeometry(200, 200, 600, 400)

        self.productos = []  # Lista de productos
        self.filtered_productos = []  # Lista filtrada para el buscador

        self.layout = QVBoxLayout()

        # Buscador
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("🔍 Buscar producto:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Escribe para filtrar...")
        self.search_input.textChanged.connect(self.filtrar_productos)
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre", "Precio", "Stock"])
        self.layout.addWidget(self.table)


        # Botones
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("➕ Agregar")
        self.edit_button = QPushButton("✏️ Editar")
        self.delete_button = QPushButton("🗑️ Eliminar")

        # Conectamos botones
        self.add_button.clicked.connect(self.agregar_producto)
        self.edit_button.clicked.connect(self.editar_producto)
        self.delete_button.clicked.connect(self.eliminar_producto)

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.filtrar_productos()

    def agregar_producto(self):
        nombre, ok = QInputDialog.getText(self, "Agregar Producto", "Nombre:")
        if ok and nombre.strip():
            precio, ok = QInputDialog.getDouble(self, "Agregar Producto", "Precio:", decimals=2)
            if ok:
                stock, ok = QInputDialog.getInt(self, "Agregar Producto", "Stock:")
                if ok:
                    self.productos.append({"nombre": nombre.strip(), "precio": precio, "stock": stock})
                    self.filtrar_productos()

    def editar_producto(self):
        fila = self.table.currentRow()
        if fila >= 0:
            producto = self.filtered_productos[fila]
            nombre, ok = QInputDialog.getText(self, "Editar Producto", "Nombre:", text=producto["nombre"])
            if ok and nombre.strip():
                precio, ok = QInputDialog.getDouble(self, "Editar Producto", "Precio:", decimals=2, value=producto["precio"])
                if ok:
                    stock, ok = QInputDialog.getInt(self, "Editar Producto", "Stock:", value=producto["stock"])
                    if ok:
                        # En lugar de reemplazar el diccionario, modificamos el original
                        producto["nombre"] = nombre.strip()
                        producto["precio"] = precio
                        producto["stock"] = stock
                        self.filtrar_productos()
        else:
            QMessageBox.warning(self, "Editar", "Selecciona un producto para editar.")


    def eliminar_producto(self):
        fila = self.table.currentRow()
        if fila >= 0:
            producto = self.filtered_productos[fila]
            respuesta = QMessageBox.question(
                self, "Eliminar Producto",
                f"¿Estás seguro de eliminar '{producto['nombre']}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.productos.remove(producto)
                self.filtrar_productos()
        else:
            QMessageBox.warning(self, "Eliminar", "Selecciona un producto para eliminar.")

    def actualizar_tabla(self):
        self.table.setRowCount(len(self.filtered_productos))
        for fila, producto in enumerate(self.filtered_productos):
            nombre_item = QTableWidgetItem(producto["nombre"])
            precio_item = QTableWidgetItem(f"{producto['precio']:.2f}")
            stock_item = QTableWidgetItem(str(producto["stock"]))

            # Colorear filas que coinciden con búsqueda
            if self.search_input.text():
                nombre_item.setBackground(QColor("#d1f0d1"))  # Verde suave
                precio_item.setBackground(QColor("#d1f0d1"))
                stock_item.setBackground(QColor("#d1f0d1"))

            self.table.setItem(fila, 0, nombre_item)
            self.table.setItem(fila, 1, precio_item)
            self.table.setItem(fila, 2, stock_item)

    def filtrar_productos(self):
        texto = self.search_input.text().lower()
        if texto:
            self.filtered_productos = [
                p for p in self.productos if texto in p["nombre"].lower()
            ]
        else:
            self.filtered_productos = self.productos.copy()
        self.actualizar_tabla()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestorProductos()
    ventana.show()
    sys.exit(app.exec_())
