-- 🎭 TEATR-AI: ARQUITECTURA TEATRAL FINAL

-- ELIMINAR (orden correcto)
DROP TABLE IF EXISTS favorites CASCADE;
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS scenes CASCADE;
DROP TABLE IF EXISTS chapters CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS obras CASCADE;

-- 1. USUARIOS
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    google_id VARCHAR(100) UNIQUE,
    email VARCHAR(100) UNIQUE,
    nombre VARCHAR(100),
    password_hash TEXT,
    rol VARCHAR(20) DEFAULT 'usuario',
    teatro_grupo VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. OBRAS_TEATRO
CREATE TABLE obras (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100),
    genero VARCHAR(50),
    dificultad VARCHAR(20),
    duracion_minutos INT,
    num_personajes INT,
    sinopsis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. CAPÍTULOS (✅ AHORA SÍ con usuario_id)
CREATE TABLE chapters (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. ESCENAS (SIN usuario_id directo - lo hereda del capítulo)
CREATE TABLE scenes (
    id SERIAL PRIMARY KEY,
    chapter_id INT REFERENCES chapters(id),
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    sources TEXT,
    obra_id INT NULL REFERENCES obras(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. FEEDBACK
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    scene_id INT UNIQUE REFERENCES scenes(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback_comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. FAVORITES
CREATE TABLE favorites (
	id SERIAL PRIMARY KEY,
    scene_id INT UNIQUE REFERENCES scenes(id),
    title VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ÍNDICES
CREATE INDEX idx_chapters_usuario_id ON chapters(usuario_id);
CREATE INDEX idx_scenes_chapter_id ON scenes(chapter_id);
CREATE INDEX idx_scenes_created_at ON scenes(created_at);
