
from xml.dom.expatbuilder import FragmentBuilder

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    outPosition =  modelMatrix * vec4(position , 1.0); 
    gl_Position = projectionMatrix *viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals =  mat3(transpose(inverse(modelMatrix))) * normals;
}

'''
#la textura solo se usa n el fragment shader
#gl_Position = modelMatrix * vec4(position + normals * sin(time * 3) / 10, 1.0); 

fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, normalize(pointLight - outPosition.xyz));
    fragColor = texture(tex, outTexCoords) * intensity;
}

'''

fat_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;


uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec3 pointLight;

void main()
{
    outPosition = modelMatrix * vec4(position + normals * sin(time * 3) / 10, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}

'''

water_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    outPosition = modelMatrix * vec4(position + vec3(0, 1, 0) *sin(time * position.x *10 ) / 10, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = normals; 
}

'''

negative_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;


uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    fragColor = 1 - texture(tex, outTexCoords);
}

'''