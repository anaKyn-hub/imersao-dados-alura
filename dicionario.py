def rename_level(df):
    rename_experience_level = {
    'SE': 'Senior',
    'MI': 'Pleno',
    'EN': 'Junior',
    'EX': 'Executive'
    }
    df["experience_level"] = df["experience_level"].replace(rename_experience_level)

def rename_companySize(df):
    rename_company_size = {
        'S': 'Pequena Empresa',
        'M': 'Média Empresa',
        'L': 'Grande Empresa'
    }
    df["company_size"] = df["company_size"].replace(rename_company_size)

def rename_remote(df):
    rename_remote_ratio = {
        0: 'Presencial',
        50: 'Hibrido',
        100: 'Remoto'
    }
    df["remote_ratio"] = df["remote_ratio"].replace(rename_remote_ratio)

def rename_emplType(df):
    rename_employment_type  =  {
        'FT': 'Tempo Integral',
        'PT': 'Meio Período',
        'FL': 'Freelance',
        'CT': 'Contrato'
    }
    df["employment_type"] = df["employment_type"].replace(rename_employment_type)