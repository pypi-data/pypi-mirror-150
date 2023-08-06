import numpy as np

import cartesio.image.kernel as k

ELLIPSE_3 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

RECT_3 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

CROSS_3 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])


class TestKernel:
    def test_clamp_ksize(self):
        assert k.clamp_ksize(0) == 3
        assert k.clamp_ksize(-10) == 3
        assert k.clamp_ksize(8) == 8
        assert k.clamp_ksize(20) == 20
        assert k.clamp_ksize(31) == 31
        assert k.clamp_ksize(32) == 31

    def test_remap_ksize(self):
        assert k.remap_ksize(255) == 31
        assert k.remap_ksize(192) == 24
        assert k.remap_ksize(128) == 17
        assert k.remap_ksize(64) == 10
        assert k.remap_ksize(0) == 3

    def test_unodd_ksize(self):
        assert k.unodd_ksize(0) == 1
        assert k.unodd_ksize(-10) == -9
        assert k.unodd_ksize(10) == 11
        assert k.unodd_ksize(5) == 5
        assert k.unodd_ksize(51) == 51

    def test_kernel_size_is_not_odd(self):
        assert k.OPENCV_MAX_KERNEL_SIZE % 2 != 0
        assert k.OPENCV_MIN_KERNEL_SIZE % 2 != 0

    def test_correct_size_all_good(self):
        assert k.correct_ksize(512) == 31
        assert k.correct_ksize(256) == 31
        assert k.correct_ksize(192) == 25
        assert k.correct_ksize(128) == 17
        assert k.correct_ksize(64) == 11
        assert k.correct_ksize(0) == 3
        assert k.correct_ksize(-1) == 3

    def test_ellipse_kernel_size(self):
        assert k.ellipse_kernel(512).shape == (31, 31)
        assert k.ellipse_kernel(256).shape == (31, 31)
        assert k.ellipse_kernel(192).shape == (25, 25)
        assert k.ellipse_kernel(128).shape == (17, 17)
        assert k.ellipse_kernel(64).shape == (11, 11)
        assert k.ellipse_kernel(0).shape == (3, 3)
        assert k.ellipse_kernel(-1).shape == (3, 3)

    def test_rect_kernel_size(self):
        assert k.rect_kernel(512).shape == (31, 31)
        assert k.rect_kernel(256).shape == (31, 31)
        assert k.rect_kernel(192).shape == (25, 25)
        assert k.rect_kernel(128).shape == (17, 17)
        assert k.rect_kernel(64).shape == (11, 11)
        assert k.rect_kernel(0).shape == (3, 3)
        assert k.rect_kernel(-1).shape == (3, 3)

    def test_cross_kernel_size(self):
        assert k.cross_kernel(512).shape == (31, 31)
        assert k.cross_kernel(256).shape == (31, 31)
        assert k.cross_kernel(192).shape == (25, 25)
        assert k.cross_kernel(128).shape == (17, 17)
        assert k.cross_kernel(64).shape == (11, 11)
        assert k.cross_kernel(0).shape == (3, 3)
        assert k.cross_kernel(-1).shape == (3, 3)

    def test_kernel_from_parameters(self):
        assert np.array_equal(ELLIPSE_3, k.kernel_from_parameters([3, 0]))
        assert np.array_equal(CROSS_3, k.kernel_from_parameters([3, 128]))
        assert np.array_equal(RECT_3, k.kernel_from_parameters([3, 192]))
