from math import pi
from pg.gl import *
import pg
import subprocess

AUDIO = '/Users/fogleman/Music/iTunes/iTunes Media/Music/John Williams/Great Composers_ John Williams/01 Star Wars_ Main Title.m4a'

class Window(pg.Window):
    def setup(self):
        # audio
        args = ['afplay', AUDIO]
        self.audio = subprocess.Popen(args)
        # title
        self.title = pg.Context(Program())
        self.title.sampler = pg.Texture(0, 'resources/crawl-pg.png',
            min_filter=GL_LINEAR_MIPMAP_LINEAR, mipmap=True)
        self.title.use_texture = True
        w, h = self.title.sampler.size
        self.title_plane = pg.Plane((0, 0, 0), (0, 0, 1), (w / 2, h / 2))
        matrix = pg.Matrix().rotate((0, 0, -1), pi / 2)
        self.title_plane = matrix * self.title_plane
        # crawl
        self.crawl = pg.Context(Program())
        self.crawl.sampler = pg.Texture(1, 'resources/crawl.png',
            min_filter=GL_LINEAR_MIPMAP_LINEAR, mipmap=True)
        self.crawl.use_texture = True
        w, h = self.crawl.sampler.size
        self.crawl_plane = pg.Plane((0, 0, 0), (0, 1, 0), (w / 2, h / 2))
        # stars
        self.stars = pg.Context(pg.TextureProgram())
        self.stars.sampler = pg.Texture(2, 'resources/crawl-stars.png')
        self.stars_sphere = pg.Sphere(4).reverse_winding()
    def teardown(self):
        self.audio.kill()
        pg.delete_all(self)
    def update(self, t, dt):
        # title
        matrix = pg.Matrix().translate((0, 0, -t * 800 + 800))
        matrix = matrix.perspective(65, self.aspect, 1, 10000)
        self.title.matrix = matrix
        self.title.opacity = max(0.0, 1.0 - (t / 11) ** 2)
        # crawl
        matrix = pg.Matrix().translate((0, -400, -t * 32 + 800))
        matrix = matrix.rotate((-1, 0, 0), pi / 8)
        matrix = matrix.perspective(65, self.aspect, 1, 10000)
        self.crawl.matrix = matrix
        if t > 60:
            self.crawl.opacity = max(0.0, 1.0 - ((t - 60) / 10) ** 2)
        else:
            self.crawl.opacity = 1.0
    def draw_stars(self):
        matrix = pg.Matrix().perspective(65, self.aspect, 0.1, 1)
        self.stars.matrix = matrix
        self.stars_sphere.draw(self.stars)
    def draw(self):
        self.clear()
        self.draw_stars()
        self.clear_depth_buffer()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.title_plane.draw(self.title)
        self.crawl_plane.draw(self.crawl)
        glEnable(GL_BLEND)

class Program(pg.BaseProgram):
    VS = '''
    #version 120

    uniform mat4 matrix;

    attribute vec4 position;
    attribute vec2 uv;

    varying vec2 frag_uv;

    void main() {
        gl_Position = matrix * position;
        frag_uv = uv;
    }
    '''
    FS = '''
    #version 120

    uniform sampler2D sampler;
    uniform float opacity;

    varying vec2 frag_uv;

    void main() {
        vec4 color = texture2D(sampler, frag_uv);
        color.a = min(color.a, opacity);
        if (color.a == 0) {
            discard;
        }
        gl_FragColor = color;
    }
    '''
    def set_defaults(self, context):
        context.opacity = 1.0

if __name__ == "__main__":
    pg.run(Window, full_screen=True)
