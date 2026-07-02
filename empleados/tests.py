from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Cargo, Empleado


class SueldoValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.client.login(username='tester', password='pass12345')
        self.cargo = Cargo.objects.create(nombre='Gerente')

    def test_negative_sueldo_rejected_vbf(self):
        resp = self.client.post('/empleados/nuevo/', {
            'nombres': 'Juan', 'apellidos': 'Perez', 'correo': 'juan@example.com',
            'sueldo': '-500', 'fecha_ingreso': '2026-01-15', 'cargo': self.cargo.pk,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'El sueldo debe ser mayor a 0.')
        self.assertFalse(Empleado.objects.filter(correo='juan@example.com').exists())

    def test_negative_sueldo_rejected_vbc(self):
        resp = self.client.post('/cbv/empleados/nuevo/', {
            'nombres': 'Maria', 'apellidos': 'Lopez', 'correo': 'maria@example.com',
            'sueldo': '-500', 'fecha_ingreso': '2026-01-15', 'cargo': self.cargo.pk,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'El sueldo debe ser mayor a 0.')
        self.assertFalse(Empleado.objects.filter(correo='maria@example.com').exists())

    def test_positive_sueldo_accepted(self):
        resp = self.client.post('/empleados/nuevo/', {
            'nombres': 'Ana', 'apellidos': 'Ruiz', 'correo': 'ana@example.com',
            'sueldo': '1500.50', 'fecha_ingreso': '2026-01-15', 'cargo': self.cargo.pk,
        })
        self.assertEqual(resp.status_code, 302)
        empleado = Empleado.objects.get(correo='ana@example.com')
        self.assertEqual(empleado.sueldo, Decimal('1500.50'))
