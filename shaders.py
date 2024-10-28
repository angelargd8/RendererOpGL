
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

#vertex
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

#vertex
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
    outPosition = modelMatrix * vec4(position + vec3(0, 1, 0) *sin(time * position.x * 5 ) / 20, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = normals; 
}

''' 

#fragment
water_color_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 cameraPosition;

out vec4 fragColor;

void main()
{
    float eta= 1.0/1.33; //indice de refraccion del agua
    
    vec3 viewDir= normalize(cameraPosition - outPosition.xyz);
    vec3 refracted = refract(viewDir, normalize(outNormals), eta );
    vec3 reflectDir = reflect(viewDir, normalize(outNormals) );
    vec3 reflectColor = texture(tex, outTexCoords + reflectDir.xy * 0.01).rgb; 
    vec3 refractColor = texture(tex, outTexCoords + refracted.xy * 0.01).rgb;

    //fresnel
    float fresnel = pow(1.0 - dot(normalize(outNormals), viewDir), 3.0);
    //colores reflejados y refractados
    vec3 color = mix(refractColor, reflectColor, fresnel);
    //color base e intensidad
    float intensity = dot(normalize(outNormals), normalize(vec3(0.0, 1.0, 0.0)));
    color = mix(color, vec3(0.0, 0.0, 1.0), 0.5) * intensity;

    fragColor = vec4(color, 1.0);



}

'''
#fragment
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

#fragment
radioactive_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 color = texture(tex, outTexCoords);
    float gray = (color.r + color.g + color.b) / 3;
    float white = 1.0 - gray;
    vec4 radioactiveColor = vec4(0.0, gray, 0.0, 1.0);

    //parpadeo
    float intensity = sin(time * 10) / 2 + 0.5;
    fragColor = mix(color, radioactiveColor, intensity);

}

'''

#fragment
distorsion_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 color = texture(tex, outTexCoords);

    color.r = sin(outPosition.y * 10.0 + time * 5.0) * 0.5 + 0.5;

    //líneas de escaneo
    float scanline = sin(outPosition.y * 50.0 + time * 10.0) * 0.1;
    color.r += scanline;

    //distorsion
    float distortion = sin(outPosition.y * 10.0 + time * 5.0) * 0.05;
    vec2 distortedTexCoords = outTexCoords + vec2(distortion, 0.0);
    color = texture(tex, distortedTexCoords);

    //brillo
    float brightness = 0.5 + 0.5 * sin(time * 2.0);
    color.r *= brightness;

    //transparencia
    color.a = 0.7;
    fragColor = color;
      


}

'''

#vertex
rotate_shader = '''
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
    vec3 pos  = position;
    float angle = time * 3;
    float c = cos(angle);
    float s = sin(angle);
    mat3 rotation = mat3(c, 0, s, 0, 1, 0, -s, 0, c);
    vec3 rotatedPos = rotation * pos;
    outPosition = modelMatrix * vec4(position + rotatedPos, 1); //+(normals/5)

    //outPosition = modelMatrix * vec4(position + normals * cos(time * 3) / 10, 2.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}

'''
#vertex
rotate1_shader = '''
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
    vec3 pos  = position;
    float angle = time * 3;
    float c = cos(angle);
    float s = sin(angle);
    mat3 rotation = mat3(c, 0, s, 0, 1, 0, -s, 0, c);
    vec3 rotatedPos = rotation * pos;
    outPosition = modelMatrix * vec4( rotatedPos, 1);

    //outPosition = modelMatrix * vec4(position + normals * cos(time * 3) / 10, 2.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}

'''
#vertex
rotate2_shader = '''
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
    vec3 pos  = position;
    float angle = time * 3;
    float c = cos(angle);
    float s = sin(angle);
    mat3 rotation = mat3(c, 0.5, s, 0.5, 1.5, 0.5, -s, 0.5, c);
    vec3 rotatedPos = rotation * pos;
    outPosition = modelMatrix * vec4(rotatedPos, 1);

    //outPosition = modelMatrix * vec4(position + normals * cos(time * 3) / 10, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}

'''
#vertex
rotate3_shader = '''
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
    vec3 pos  = position;
    float angle = time * 3;
    float c = cos(angle);
    float s = sin(angle);
    mat3 rotation = mat3(c, 0, s, 0, 1, 0, -s, 0, c);
    vec3 rotatedPos = rotation * pos;
    outPosition = modelMatrix * vec4(position +normals + rotatedPos, 3);

    //outPosition = modelMatrix * vec4(position + normals * cos(time * 3) / 10, 2.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}

'''
#vertex
close_shader = '''
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
    vec3 pos  = position;
    outPosition = modelMatrix * vec4( (position*5) * cos(time) , 1); //+(normals/5) /(normals*10) 
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}


'''

#fragment
rainbow_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main()
{
    vec4 color = texture(tex, outTexCoords);
    float hue = mod(time * 3, 1.0);
    vec3 rainbowColor = hsv2rgb(vec3(hue, 1.0, 1.0)); // Saturación y valor fijos
    //color de la textura con el color arcoiris
    fragColor= mix(color, vec4(rainbowColor, 1.0), 0.5);
}

'''