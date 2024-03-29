# CG-Rasterisation-Engine

Reconstructed the OpenGL API in Python
and implemented the  pipeline to render 2D and 3D models in the engine.
The engine is also capable of rendering models with textures and shading.

## Rendering Pipeline

![gl_pipeline](https://github.com/nehaask/CG-Rasterisation-Engine/assets/60215440/cdc9fe22-1e80-4649-8d37-05005b57eb84)

Use this for pipeline reference
(cc: http://www.songho.ca/opengl/gl_pipeline.html)
## Features

- Line Rasterisation using the Bresenham's Line Algorithm
- Triangle Rasterisation using the Edge function and Barycentric Coordinates
- Line Clipping using the Cohen-Sutherland Algorithm
- Polygon Clipping using the Sutherland-Hodgman Algorithm
- Transformations: Translation, Scaling, Rotation using Homogenous coordinates
- Converting 2D engine to 3D engine by OpenGL standards
- 3D Rasterisation using the Z-Buffer Algorithm
- 3D Transformation using Hierarchical modeling
- Introducing a Camera in the 3D engine
- 3D Projection using Perspective and Orthographic Projection
- Illumination: Angular, Specular and Diffuse Illumination
- Shading using Gouroud and Phong's Model
- Texture Mapping using Procedural and Stored textures


