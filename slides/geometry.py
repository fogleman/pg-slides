from pg.gl import *
import pg

class Window(pg.Window):
    def setup(self):
        self.camera = pg.Camera()
        position = pg.mul(pg.normalize((-1, 0.5, 1)), 3)
        self.camera.look_at(position, (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        shapes = [
            pg.Sphere(4, 0.5, (0, 0, 0)),
            pg.Cone((0, 0.5, 0), (0, -0.5, 0), 0.5, 36),
            pg.Cuboid(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5),
            pg.Cylinder((0, -0.5, 0), (0, 0.5, 0), 0.5, 36),
        ]
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.shapes = []
        for (dx, dz), shape in zip(offsets, shapes):
            m = 1.5
            matrix = pg.Matrix().translate((dx * m, 0, dz * m))
            shape = matrix * shape
            self.shapes.append(shape)
    def teardown(self):
        pg.delete_all(self)
        for shape in self.shapes:
            shape.delete()
    def update(self, t, dt):
        matrix = pg.Matrix().rotate((0, 1, 0), t / 4)
        self.context.light_direction = matrix.inverse() * pg.normalize((1, 1, 1))
        self.context.camera_position = matrix.inverse() * self.camera.position
        matrix = self.camera.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        if (t / 4) % 2.0 < 1.0:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    def draw(self):
        self.clear()
        for shape in self.shapes:
            shape.draw(self.context)

if __name__ == "__main__":
    pg.run(Window, full_screen=True)
