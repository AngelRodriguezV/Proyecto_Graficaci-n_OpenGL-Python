
vertex_shader = """
# version 330 core

layout(location = 0) in vec3 a_position; // Vector del vertice
layout(location = 1) in vec2 a_texture; // Vector de la textura
layout(location = 2) in vec3 a_normal; // Vector de las normals
layout(location = 3) in vec3 a_color; // Vector del color

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec3 v_color;
out vec3 v_normal;
out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
    v_color = a_color;
    v_normal = a_normal;
}
"""

fragment_shader = """
# version 330 core

in vec2 v_texture;
in vec3 v_color;
in vec3 v_normal;

out vec4 out_color;

uniform int switcher;
uniform sampler2D s_texture;

void main()
{
    if (switcher == 0){
        out_color = texture(s_texture, v_texture);
    }
    else if (switcher == 1){
        out_color = vec4(v_color, 1.0);   
    }
}
"""

vertexLight_shader = """
# version 330 core

layout(location = 0) in vec3 a_position; // Vector del vertice
layout(location = 1) in vec2 a_texture; // Vector de la textura
layout(location = 2) in vec3 a_normal; // Vector de las normals
layout(location = 3) in vec3 a_color; // Vector del color

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 light;

out vec3 v_color;
out vec3 v_normal;
out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
    v_color = a_color;
    v_normal = (light * vec4(a_normal, 0.0)).xyz;
}
"""

fragmentLight_shader = """
# version 330 core

in vec2 v_texture;
in vec3 v_color;
in vec3 v_normal;

out vec4 out_color;

uniform int switcher;
uniform sampler2D s_texture;

void main()
{
    vec3 ambientLightIntensity = vec3(0.3f, 0.2f, 0.4f);
    vec3 sunLightIntensity = vec3(0.9f, 0.9f, 0.9f);
    vec3 sunLightDirection = normalize(vec3(-2.0f, -2.0f, 0.0f));

    vec3 lightIntensity = ambientLightIntensity + sunLightIntensity * max(dot(v_normal, sunLightDirection), 0.0f);

    vec4 texel = texture(s_texture, v_texture);

    if (switcher == 0){
        out_color = vec4(texel.rgb * lightIntensity, texel.a);
    }
    else if (switcher == 1){
        out_color = vec4(v_color * lightIntensity, 1.0);   
    }
}
"""