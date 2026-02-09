
# HU-001: Seleccionar perfil

# 🔴 HU-001 CASO ROJO 1: seleccionar sin perfiles
def test_hu001_rojo_sin_perfiles(self):
    perfil = self.tm.seleccionar_perfil(1)
    self.assertIsNone(perfil)
