""" Program to apply filters"""
import numpy as np

def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """Apply given filter on image."""
    assert image.ndim in [2, 3]
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]

    image = image.astype(np.float64)

    def pad_image(image, kernel):
        pad_size = kernel.shape[0] // 2
        if image.ndim == 3:
            result = np.pad(image, ((pad_size, pad_size),
                                  (pad_size, pad_size), (0, 0)), mode='constant')
        else:
            result = np.pad(image, pad_size, mode='constant')
        return result
    padded_image = pad_image(image, kernel)

    result = np.zeros_like(image)

    for c in range(1 if image.ndim == 2 else image.shape[2]):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image.ndim == 3:
                    sub_image = padded_image[i:i + kernel.shape[0], j:j + kernel.shape[1], c]
                else:
                    sub_image = padded_image[i:i + kernel.shape[0], j:j + kernel.shape[1]]
                convolution_result = np.sum(kernel * sub_image)
                if image.ndim == 2:
                    result[i, j] = convolution_result
                else:
                    result[i, j, c] = convolution_result

    return np.clip(result, 0, 255).astype(np.uint8)
