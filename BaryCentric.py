from LineDrawAlgorithm import Image
import numpy as np




class BaryCentricTriangle(object):
    def cross_product(self, x, y):
        u = np.array([x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0]])
        return u

    def barycentric(self, pts, p):
        x = np.array([pts[2][0]-pts[0][0], pts[1][0]-pts[0][0], pts[0][0]-p[0]])
        y = np.array([pts[2][1]-pts[0][1], pts[1][1]-pts[0][1], pts[0][1]-p[1]])
        u = self.cross_product(x, y)
        if abs(u[2]) < 1:
            m = np.array([-1, 1, 1])
            return m
        m = np.array([1 - (u[0] + u[1])/u[2], u[1]/u[2], u[0]/u[2]])
        return m

    def triangle(self, pts, image, color):
        bboxmin = np.array([image.width - 1, image.height])
        bboxmax = np.array([0, 0])
        clamp = np.array([image.width - 1, image.height])
        for i in range(0, 3):
            for j in range(0, 2):
                bboxmin[j] = max(0, min(bboxmin[j], pts[i][j]))
                bboxmax[j] = min(clamp[j], max(bboxmax[j], pts[i][j]))
        p = [[], []]
        for p[0] in range(bboxmin[0], bboxmax[0] + 1):
            for p[1] in range(bboxmin[1], bboxmax[1] + 1):
                bc_screen = self.barycentric(pts, p)
                if bc_screen[0] < 0 or bc_screen[1] < 0 or bc_screen[2] < 0:
                    continue
                image.set_pixel(p[0], p[1], color)

    def face_triangle(self, image, obj_file, width, height):
        light_dir = np.array([0, 0, -1])
        vertices, faces = image.open_file(obj_file)
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
                screen_coords[j] = [(world_coords[j][0] + 1) * width / 2, (world_coords[j][1] + 1) * height / 2]
            # BaryCentricTriangle.triangle(screen_coords, image, BaryCentricTriangle, np.random.randint(256, size=3))

            n = np.cross(world_coords[2] - world_coords[0], world_coords[1] - world_coords[0])
            n_norm = n / np.linalg.norm(n)
            intensity = np.dot(n_norm, light_dir)
            if intensity > 0:
                self.triangle(screen_coords, image, (intensity * 255, intensity * 255, intensity * 255))




if __name__ == '__main__':
    barycentric = BaryCentricTriangle()
    triangle_image = Image(1024, 1024)
    '''
    pts = np.array([[10, 10], [100, 30], [190, 160]])
    barycentric.triangle(pts, triangle_image, barycentric, (255, 0, 0))
    triangle_image.write("barycentric.jpg")
    '''
    barycentric.face_triangle(triangle_image, "african_head.obj", triangle_image.width, triangle_image.height)
    # triangle_image.write("face_triangle.jpg")
    triangle_image.write("face_triangle_light.jpg")