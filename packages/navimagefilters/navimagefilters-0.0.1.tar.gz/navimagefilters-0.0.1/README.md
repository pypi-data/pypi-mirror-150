# Image Filters

This package contains simple image filters

### How to Use?
```python
import cv2
from facefilters.main import edge_detect

# change the algorithm to get different edge detections
img = edge_detect('example.jpg', algorithm="canny", show=False)

cv2.imwrite('image.jpg', img)

```