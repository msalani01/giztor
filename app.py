import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog, QDialog
)
from PyQt5.QtGui import QColor

class GestorProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛒 Gestor de Productos V4")
        self.setGeometry(200, 200, 600, 400)

        self.productos = []
        self.filtered_productos = []
        self.ventas = []

        self.cargar_datos()
        self.cargar_ventas()

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
        self.table.setEditTriggers(self.table.NoEditTriggers)

        # Botones
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("➕ Agregar")
        self.edit_button = QPushButton("✏️ Editar")
        self.delete_button = QPushButton("🗑️ Eliminar")
        self.sale_button = QPushButton("💵 Registrar Venta")
        self.view_sales_button = QPushButton("📄 Ver Ventas")

        # Conectar botones
        self.add_button.clicked.connect(self.agregar_producto)
        self.edit_button.clicked.connect(self.editar_producto)
        self.delete_button.clicked.connect(self.eliminar_producto)
        self.sale_button.clicked.connect(self.registrar_venta)
        self.view_sales_button.clicked.connect(self.ver_ventas)

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.sale_button)
        self.button_layout.addWidget(self.view_sales_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.filtrar_productos()

    def cargar_datos(self):
        try:
            with open("productos.json", "r") as f:
                self.productos = json.load(f)
        except FileNotFoundError:
            self.productos = []

    def guardar_datos(self):
        with open("productos.json", "w") as f:
            json.dump(self.productos, f, indent=4)

    def cargar_ventas(self):
        try:
            with open("ventas.json", "r") as f:
                self.ventas = json.load(f)
        except FileNotFoundError:
            self.ventas = []

    def guardar_ventas(self):
        with open("ventas.json", "w") as f:
            json.dump(self.ventas, f, indent=4)

    def agregar_producto(self):
        nombre, ok = QInputDialog.getText(self, "Agregar Producto", "Nombre:")
        if ok and nombre.strip():
            precio, ok = QInputDialog.getDouble(self, "Agregar Producto", "Precio:", decimals=2)
            if ok:
                stock, ok = QInputDialog.getInt(self, "Agregar Producto", "Stock:")
                if ok:
                    self.productos.append({"nombre": nombre.strip(), "precio": precio, "stock": stock})
                    self.guardar_datos()
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
                        producto["nombre"] = nombre.strip()
                        producto["precio"] = precio
                        producto["stock"] = stock
                        self.guardar_datos()
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
                self.guardar_datos()
                self.filtrar_productos()
        else:
            QMessageBox.warning(self, "Eliminar", "Selecciona un producto para eliminar.")

    def registrar_venta(self):
        fila = self.table.currentRow()
        if fila >= 0:
            producto = self.filtered_productos[fila]
            cantidad, ok = QInputDialog.getInt(self, "Registrar Venta", "Cantidad vendida:", min=1)
            if ok:
                if cantidad > producto["stock"]:
                    QMessageBox.warning(self, "Stock insuficiente", f"No hay suficiente stock de '{producto['nombre']}'")
                    return
                producto["stock"] -= cantidad
                venta = {
                    "producto": producto["nombre"],
                    "cantidad": cantidad,
                    "precio_unitario": producto["precio"],
                    "total": producto["precio"] * cantidad,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.ventas.append(venta)
                self.guardar_datos()
                self.guardar_ventas()
                self.filtrar_productos()
                QMessageBox.information(self, "Venta Registrada", f"Venta de {cantidad} x '{producto['nombre']}' registrada.")
        else:
            QMessageBox.warning(self, "Registrar Venta", "Selecciona un producto para registrar la venta.")

    def ver_ventas(self):
        if not self.ventas:
            QMessageBox.information(self, "Ventas", "No hay ventas registradas.")
            return

        dialogo = QDialog(self)
        dialogo.setWindowTitle("📄 Resumen de Ventas")
        dialogo.setGeometry(250, 250, 500, 300)
        layout = QVBoxLayout()

        tabla = QTableWidget()
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels(["Producto", "Cantidad", "Total", "Fecha"])
        tabla.setRowCount(len(self.ventas))

        for fila, venta in enumerate(self.ventas):
            tabla.setItem(fila, 0, QTableWidgetItem(venta["producto"]))
            tabla.setItem(fila, 1, QTableWidgetItem(str(venta["cantidad"])))
            tabla.setItem(fila, 2, QTableWidgetItem(f"{venta['total']:.2f}"))
            tabla.setItem(fila, 3, QTableWidgetItem(venta["fecha"]))

        tabla.resizeColumnsToContents()
        layout.addWidget(tabla)

        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.clicked.connect(dialogo.accept)
        layout.addWidget(cerrar_btn)

        dialogo.setLayout(layout)
        dialogo.exec_()

    def actualizar_tabla(self):
        self.table.setRowCount(len(self.filtered_productos))
        for fila, producto in enumerate(self.filtered_productos):
            nombre_item = QTableWidgetItem(producto["nombre"])
            precio_item = QTableWidgetItem(f"{producto['precio']:.2f}")
            stock_item = QTableWidgetItem(str(producto["stock"]))

            if self.search_input.text():
                nombre_item.setBackground(QColor("#d1f0d1"))
                precio_item.setBackground(QColor("#d1f0d1"))
                stock_item.setBackground(QColor("#d1f0d1"))

            self.table.setItem(fila, 0, nombre_item)
            self.table.setItem(fila, 1, precio_item)
            self.table.setItem(fila, 2, stock_item)

    def filtrar_productos(self):
        texto = self.search_input.text().lower()
        if texto:
            self.filtered_productos = [p for p in self.productos if texto in p["nombre"].lower()]
        else:
            self.filtered_productos = self.productos.copy()
        self.actualizar_tabla()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestorProductos()
    ventana.show()
    sys.exit(app.exec_())
