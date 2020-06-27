from LineDrawAlgorithm import Image
from BaryCentric import BaryCentricTriangle
import numpy as np
import skimage.io as sio
import re

height = 800
width = 800
depth = 255

camera = np.array([0, 0, 3])



class Texture(object):

    def open_file(self, obj_file):
        with open (obj_file, 'r') as obj:
            data = obj.read()
        lines = data.splitlines()
        texture = []
        faces = []
        vertices = []
        for line in lines:
            if line:
                if line[1] == 't':
                    texture.append(line[4:])
                elif line[0] == 'f':
                    line_f = re.split('/| ', line)
                    faces.append([line_f[1], line_f[4], line_f[7], line_f[2], line_f[5], line_f[8]])
                elif line[0] == 'v':
                    vertices.append(line[2:])
        return texture, faces, vertices

    def get_color(self, ver0, ver1, ver2, texture, image_texture):
        color = []
        textimg_width = image_texture.shape[1]
        textimg_height = image_texture.shape[0]
        ver0_x = int(float(texture[ver0].split()[0]) * textimg_width)
        ver0_y = int(float(texture[ver0].split()[1]) * textimg_height)
        ver1_x = int(float(texture[ver1].split()[0]) * textimg_width)
        ver1_y = int(float(texture[ver1].split()[1]) * textimg_height)
        ver2_x = int(float(texture[ver2].split()[0]) * textimg_width)
        ver2_y = int(float(texture[ver2].split()[1]) * textimg_height)
        ver0_color = image_texture[ver0_x][ver0_y]
        ver1_color = image_texture[ver1_x][ver1_y]
        ver2_color = image_texture[ver2_x][ver2_y]
        for i in range(0, 3):
            color_each = int((float(ver0_color[i]) + float(ver1_color[i]) + float(ver2_color[i])) / 3)
            color.append(color_each)
        return color



    def triangle(self, pts, image, zbuffer, BaryCentricTriangle, color):
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

    def face_zbuff(self, image, obj_file, BaryCentricTriangle, camera):
        light_dir = np.array([0, 0, -1])
        texture, faces, vertices = self.open_file(obj_file)
        zbuffer = np.zeros(shape=(image.width * image.height)) - np.inf
        image_texture = sio.imread('african_head_diffuse.tga', plugin='matplotlib')

        c = camera[2]

        for face in faces:
            screen_coords = [[], [], []]
            shape_ver0 = int(face[0]) - 1
            shape_ver1 = int(face[1]) - 1
            shape_ver2 = int(face[2]) - 1
            texture_ver0 = int(face[3]) - 1
            texture_ver1 = int(face[4]) - 1
            texture_ver2 = int(face[5]) - 1
            color = self.get_color(texture_ver0, texture_ver1, texture_ver2, texture, image_texture)
            world_coords = np.array([[float(vertices[shape_ver0].split()[0]),
                                      float(vertices[shape_ver0].split()[1]),
                                      float(vertices[shape_ver0].split()[2])
                                      ],
                                     [float(vertices[shape_ver1].split()[0]),
                                      float(vertices[shape_ver1].split()[1]),
                                      float(vertices[shape_ver1].split()[2])
                                      ],
                                     [float(vertices[shape_ver2].split()[0]),
                                      float(vertices[shape_ver2].split()[1]),
                                      float(vertices[shape_ver2].split()[2])
                                      ]
                                     ])

            for j in range(0, 3):
                perspective_mat = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 1, 0],
                                            [0, 0, -1/c, 1]])
                matrix_4d = np.array([world_coords[j][0], world_coords[j][1], world_coords[j][2], 1])
                result_4d = np.dot(perspective_mat, matrix_4d)
                world_coords[j] = np.array([result_4d[0] / result_4d[3], result_4d[1] / result_4d[3], result_4d[2] / result_4d[3]])
                screen_coords[j] = [(world_coords[j][0] + 1) * image.width / 2,
                                    (world_coords[j][1] + 1) * image.height / 2,
                                    world_coords[j][2]]


            # BaryCentricTriangle.triangle(screen_coords, image, BaryCentricTriangle, np.random.randint(256, size=3))

            n = np.cross(world_coords[2] - world_coords[0], world_coords[1] - world_coords[0])
            n_norm = n / np.linalg.norm(n)
            intensity = np.dot(n_norm, light_dir)
            if intensity > 0:
                self.triangle(screen_coords, image, zbuffer, BaryCentricTriangle, (intensity * color[0], intensity * color[1], intensity * color[2]))


if __name__ == '__main__':
    image = Image(1024, 1024)
    barycentric = BaryCentricTriangle()
    textures = Texture()
    textures.face_zbuff(image, "african_head.obj", barycentric, camera)
    image.write("face_perspective.jpg")