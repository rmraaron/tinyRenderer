import numpy as np
import cProfile
import re
import skimage.io as sio


RED = (255, 0, 0)
WHITE = (255, 255, 255)


class Image(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height - 1
        self.pixels = np.zeros(shape=(height, width, 3), dtype=np.float)

    def write(self, filename):
        sio.imsave(filename, self.pixels)

    def set_pixel(self, x, y, colour):
        self.pixels[self.height - y, x, :] = colour

    def draw_line(self, x0, y0, x1, y1, colour):
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0
        derror2 = abs(dy) * 2
        error2 = 0
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                self.set_pixel(int(y), int(x), colour)
            else:
                self.set_pixel(int(x), int(y), colour)

            error2 += derror2
            if error2 > dx:
                y += (1 if y1 > y0 else -1)
                error2 -= dx *2

    def open_file(self, obj_file):
        with open (obj_file, 'r') as obj:
            data = obj.read()
        lines = data.splitlines()
        vertices = []
        faces = []
        for line in lines:
            if line:
                if line[0] == 'v':
                    vertices.append(line[2:])
                elif line[0] == 'f':
                    line_f = re.split('/| ', line)
                    faces.append([line_f[1], line_f[4], line_f[7]])
        return vertices, faces


    def draw_triangle_wireframe(self, obj_file):
        vertices, faces = self.open_file(obj_file)
        for face in faces:
            ver0 = int(face[0]) - 1
            ver1 = int(face[1]) - 1
            ver2 = int(face[2]) - 1

            self.draw_line(int((float(vertices[ver0].split()[0]) + 1.) * self.width / 2),
                           int((float(vertices[ver0].split()[1]) + 1.) * self.height / 2),
                           int((float(vertices[ver1].split()[0]) + 1) * self.width / 2),
                           int((float(vertices[ver1].split()[1]) + 1) * self.height / 2), WHITE)
            self.draw_line(int((float(vertices[ver0].split()[0]) + 1.) * self.width / 2),
                           int((float(vertices[ver0].split()[1]) + 1.) * self.height / 2),
                           int((float(vertices[ver2].split()[0]) + 1) * self.width / 2),
                           int((float(vertices[ver2].split()[1]) + 1) * self.height / 2), WHITE)
            self.draw_line(int((float(vertices[ver1].split()[0]) + 1.) * self.width / 2),
                           int((float(vertices[ver1].split()[1]) + 1.) * self.height / 2),
                           int((float(vertices[ver2].split()[0]) + 1) * self.width / 2),
                           int((float(vertices[ver2].split()[1]) + 1) * self.height / 2), WHITE)


# triangle("african_head.obj")

'''
if __name__ == '__main__':
    head_image = Image(1024, 1024)
    # head_image.draw_line(0, 0, 1023, 1023, WHITE)
    head_image.draw_triangle_wireframe("african_head.obj")
    head_image.write("african_head.jpg")
'''