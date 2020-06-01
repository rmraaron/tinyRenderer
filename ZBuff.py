from LineDrawAlgorithm import Image
from BaryCentric import BaryCentricTriangle
import numpy as np


'''
scene = Image(1024, 1024)
scene.draw_line(20, 34, 744, 400, (255, 0, 0))
scene.draw_line(120, 434, 444, 400, (0, 255, 0))
scene.draw_line(330, 463, 594, 200, (0, 0, 255))
scene.draw_line(10, 10, 790, 10, (255, 255, 255))

scene.write("scene.jpg")
'''

height = 800
width = 800


class ZBuff(object):

    def rasterize(self, p0, p1, image, color, ybuffer):
        if p0[0] > p1[0]:
            p0, p1 = p1, p0
        for x in range(p0[0], p1[0] + 1):
            t = (x - p0[0]) / (p1[0] - p0[0])
            y = p0[1] * (1 - t) + p1[1] * t
            if ybuffer[x] < y:
                ybuffer[x] = y
                image.set_pixel(x, 0, color)

    def render(self, width):
        image = Image(width, 16)
        ybuffer = []
        for i in range(0, width):
            ybuffer.append(-2147483648)
        self.rasterize([20, 34], [744, 400], image, (255, 0, 0), ybuffer)
        self.rasterize([120, 434], [444, 400], image, (0, 255, 0), ybuffer)
        self.rasterize([330, 463], [594, 200], image, (0, 0, 255), ybuffer)

        image.write('render.jpg')

    def triangle(self, pts, image, color, zbuffer, BaryCentricTriangle):
        bboxmin = np.array([np.inf, np.inf])
        bboxmax = np.array([-np.inf, -np.inf])
        clamp = np.array([image.width - 1, image.height])
        for i in range(0, 3):
            for j in range(0, 2):
                bboxmin[j] = max(0, min(bboxmin[j], pts[i][j]))
                bboxmax[j] = min(clamp[j], max(bboxmax[j], pts[i][j]))
        p = [[], [], []]
        for p[0] in range(int(bboxmin[0]), int(bboxmax[0]) + 1):
            for p[1] in range(int(bboxmin[1]), int(bboxmax[1] + 1)):
                bc_screen = BaryCentricTriangle.barycentric(pts, p)
                if bc_screen[0] < 0 or bc_screen[1] < 0 or bc_screen[2] < 0:
                    continue
                p[2] = 0
                for i in range(0, 3):
                    p[2] += pts[i][2] * bc_screen[i]
                if zbuffer[p[0] + p[1] * width] < p[2]:
                    zbuffer[p[0] + p[1] * width] = p[2]
                    image.set_pixel(p[0], p[1], color)

    def face_zbuff(self, image, obj_file, BaryCentricTriangle):
        light_dir = np.array([0, 0, -1])
        vertices, faces = image.open_file(obj_file)
        zbuffer = np.zeros(shape=(image.width * image.height)) - np.inf

        for face in faces:
            screen_coords = [[], [], []]
            ver0 = int(face[0]) - 1
            ver1 = int(face[1]) - 1
            ver2 = int(face[2]) - 1
            world_coords = np.array([[float(vertices[ver0].split()[0]),
                                      float(vertices[ver0].split()[1]),
                                      float(vertices[ver0].split()[2])],
                                     [float(vertices[ver1].split()[0]),
                                      float(vertices[ver1].split()[1]),
                                      float(vertices[ver1].split()[2])],
                                     [float(vertices[ver2].split()[0]),
                                      float(vertices[ver2].split()[1]),
                                      float(vertices[ver2].split()[2])]])
            for j in range(0, 3):
                screen_coords[j] = [(world_coords[j][0] + 1) * image.width / 2,
                                    (world_coords[j][1] + 1) * image.height / 2,
                                    world_coords[j][2]]
            # BaryCentricTriangle.triangle(screen_coords, image, BaryCentricTriangle, np.random.randint(256, size=3))

            n = np.cross(world_coords[2] - world_coords[0], world_coords[1] - world_coords[0])
            n_norm = n / np.linalg.norm(n)
            intensity = np.dot(n_norm, light_dir)
            if intensity > 0:
                self.triangle(screen_coords, image, (intensity * 255, intensity * 255, intensity * 255), zbuffer, BaryCentricTriangle)


if __name__ == '__main__':
    image = Image(1024, 1024)
    barycentric = BaryCentricTriangle()
    zbuff = ZBuff()
    zbuff.face_zbuff(image, "african_head.obj", barycentric)
    image.write("face_zbuff.jpg")