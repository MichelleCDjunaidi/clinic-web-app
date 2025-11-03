CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diagnosis_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consultations (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    patient_name VARCHAR(255) NOT NULL,
    consultation_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consultation_diagnoses (
    id SERIAL PRIMARY KEY,
    consultation_id INTEGER REFERENCES consultations(id) ON DELETE CASCADE,
    diagnosis_code_id INTEGER REFERENCES diagnosis_codes(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert 100 ICD-10 codes (took only headers for simplicity)
INSERT INTO diagnosis_codes (code, description) VALUES
('A00', 'Cholera'),
('A01', 'Typhoid and paratyphoid fevers'),
('A02', 'Other salmonella infections'),
('A03', 'Shigellosis'),
('A04', 'Other bacterial intestinal infections'),
('A05', 'Other bacterial foodborne intoxications'),
('A06', 'Amebiasis'),
('A07', 'Other protozoal intestinal diseases'),
('A08', 'Viral and other specified intestinal infections'),
('A09', 'Infectious gastroenteritis and colitis'),
('A15', 'Respiratory tuberculosis'),
('A16', 'Respiratory tuberculosis, not confirmed'),
('A17', 'Tuberculosis of nervous system'),
('A18', 'Tuberculosis of other organs'),
('A19', 'Miliary tuberculosis'),
('A20', 'Plague'),
('A21', 'Tularemia'),
('A22', 'Anthrax'),
('A23', 'Brucellosis'),
('A24', 'Glanders and melioidosis'),
('A25', 'Rat-bite fevers'),
('A26', 'Erysipeloid'),
('A27', 'Leptospirosis'),
('A28', 'Other zoonotic bacterial diseases'),
('A30', 'Leprosy'),
('A31', 'Infection due to other mycobacteria'),
('A32', 'Listeriosis'),
('A33', 'Tetanus neonatorum'),
('A34', 'Obstetrical tetanus'),
('A35', 'Other tetanus'),
('A36', 'Diphtheria'),
('A37', 'Whooping cough'),
('A38', 'Scarlet fever'),
('A39', 'Meningococcal infection'),
('A40', 'Streptococcal sepsis'),
('A41', 'Other sepsis'),
('A42', 'Actinomycosis'),
('A43', 'Nocardiosis'),
('A44', 'Bartonellosis'),
('A46', 'Erysipelas'),
('A48', 'Other bacterial diseases'),
('A49', 'Bacterial infection of unspecified site'),
('A50', 'Congenital syphilis'),
('A51', 'Early syphilis'),
('A52', 'Late syphilis'),
('A53', 'Other and unspecified syphilis'),
('A54', 'Gonococcal infection'),
('A55', 'Chlamydial lymphogranuloma'),
('A56', 'Other sexually transmitted chlamydial diseases'),
('A57', 'Chancroid'),
('A58', 'Granuloma inguinale'),
('A59', 'Trichomoniasis'),
('A60', 'Anogenital herpesviral infection'),
('A63', 'Other predominantly sexually transmitted diseases'),
('A64', 'Unspecified sexually transmitted disease'),
('A65', 'Nonvenereal syphilis'),
('A66', 'Yaws'),
('A67', 'Pinta'),
('A68', 'Relapsing fevers'),
('A69', 'Other spirochetal infections'),
('A70', 'Chlamydia psittaci infections'),
('A71', 'Trachoma'),
('A74', 'Other diseases caused by chlamydiae'),
('A75', 'Typhus fever'),
('A77', 'Spotted fever'),
('A78', 'Q fever'),
('A79', 'Other rickettsioses'),
('A80', 'Acute poliomyelitis'),
('A81', 'Atypical virus infections of central nervous system'),
('A82', 'Rabies'),
('A83', 'Mosquito-borne viral encephalitis'),
('A84', 'Tick-borne viral encephalitis'),
('A85', 'Other viral encephalitis'),
('A86', 'Unspecified viral encephalitis'),
('A87', 'Viral meningitis'),
('A88', 'Other viral infections of central nervous system'),
('A89', 'Unspecified viral infection of central nervous system'),
('A90', 'Dengue fever'),
('A91', 'Dengue hemorrhagic fever'),
('A92', 'Other mosquito-borne viral fevers'),
('A93', 'Other arthropod-borne viral fevers'),
('A94', 'Unspecified arthropod-borne viral fever'),
('A95', 'Yellow fever'),
('A96', 'Arenaviral hemorrhagic fever'),
('A98', 'Other viral hemorrhagic fevers'),
('A99', 'Unspecified viral hemorrhagic fever'),
('B00', 'Herpesviral infections'),
('B01', 'Varicella'),
('B02', 'Zoster'),
('B03', 'Smallpox'),
('B04', 'Monkeypox'),
('B05', 'Measles'),
('B06', 'Rubella'),
('B07', 'Viral warts'),
('B08', 'Other viral infections characterized by skin lesions'),
('B09', 'Unspecified viral infection characterized by skin lesions'),
('B10', 'Other human herpesviruses'),

-- since most of the operations on these would be queries, it's okay for the insert to be slow
CREATE INDEX idx_diagnosis_code ON diagnosis_codes(code);
CREATE INDEX idx_diagnosis_description ON diagnosis_codes(description);
CREATE INDEX idx_consultation_date ON consultations(consultation_date);
CREATE INDEX idx_doctor_email ON doctors(email);

-- this is actually password123
INSERT INTO doctors (email, full_name, hashed_password) VALUES
('doctor@example.com', 'John Enak', '$2b$12$fBcJwa157RQBHorbQe4uwOKHulQgrnQP41VujUu.Es3ueT6el7nIm');