# SRE Guide - Amara (Vestra)

Guía operacional para ingenieros de SRE sobre la infraestructura, CI/CD y deployment de Amara.

---

## 1. Repositorio & Versionado

**Repo**: `https://github.com/vertexcreations/amara.git`  
**Branch principal**: `main`  
**Política**: Squash or merge en PRs, committs limpios con prefijos convencionales.

### Historial de Migración

- **Fecha**: 15 de Junio, 2026
- **De**: `https://github.com/vertexcreations/AppPoS_2.git`
- **A**: `https://github.com/vertexcreations/amara.git`
- **Archivos de config agregados**:
  - `.gitignore` - Excluye `.venv*/`, `dist/`, `build/`, `__pycache__/`, etc.
  - `.github/workflows/ci.yml` - Pipeline de tests en Ubuntu + Python 3.11
  - `requirements-dev.txt` - pytest, pytest-flask
  - `README.md` - Secciones actualizadas con CI/CD y testing

### Limpieza Inicial

Se removieron ~7K archivos de venv-related (`.venv/`, `.venv311/`) del historio de git.

---

## 2. CI/CD Pipeline

### GitHub Actions Workflow

**Ubicación**: `.github/workflows/ci.yml`

**Trigger**:
- `push` a `main`
- `pull_request` hacia `main`

**Job: `test`**
- Runs on: `ubuntu-latest`
- Python: `3.11`
- Steps:
  1. Checkout código
  2. Setup Python 3.11 (con pip cache)
  3. Install requirements.txt + requirements-dev.txt
  4. `pytest tests/ -v` (verbose)
  5. Coverage report (optional, non-blocking)

**Badge/Status**:
- GitHub Actions tab: https://github.com/vertexcreations/amara/actions
- Status en PRs: automático, bloquea merge si falla

### Ejecución Local (pre-push)

```bash
# Setup
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=. --cov-report=term-missing
```

---

## 3. Ambiente de Distribución

### Build Local (.exe)

**Platform**: Windows (requiere Windows para PyInstaller)  
**Entry Point**: `desktop_app.py`  
**Config**: `amara.spec` (PyInstaller spec)

**Build Command**:
```bash
python build_exe.py
```

**Output**: `dist/amara.exe` (~20 MB)

**Nota**: El .exe NO está en git (excluido por .gitignore). Se distribuye via GitHub Releases manual o auto-release workflow (future).

### PyInstaller Config

**`amara.spec`** bundea:
- `templates/` - HTML
- `static/` - CSS, JS, assets
- Hidden imports: `pywebview`

**Entorno de Build**:
- Python 3.11
- PyInstaller >= 6.0
- Windows 10/11 (x64)

### Future: Auto-Release Workflow

Cuando se implemente, el workflow compilará en `windows-latest` runner y publicará en GitHub Releases con:
- Trigger: Tag `v*` (semver)
- Output: Release notes + amara.exe attachment
- Artifact retention: 90 días

---

## 4. Dependencias & Versiones

### Production (`requirements.txt`)
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
```

### Development (`requirements-dev.txt`)
```
-r requirements.txt
pytest==8.0.0
pytest-flask==1.3.0
```

### Python Target
- **Local Dev**: 3.11 (recomendado)
- **CI**: 3.11
- **Min Supported**: 3.8 (según README, pero CI valida 3.11)

**Upgrade Path**: Si se cambia a 3.12+, actualizar:
- `.github/workflows/ci.yml`: `python-version: ["3.12"]`
- `README.md`: Documentación
- `requirements*.txt`: Re-test dependencies

---

## 5. Base de Datos

### Estructura

**Type**: SQLite  
**Location**: `instance/pos.db` (creada al startup)  
**Models**: `models.py` (Product, Category, Sale, SaleItem, Merchandise, etc.)

**ORM**: SQLAlchemy + Flask-SQLAlchemy

### Testing

- Tests usan BD en memoria: `sqlite:///:memory:`
- Fixtures en `tests/conftest.py` manejan setup/teardown
- No hay migrations (SQLAlchemy `create_all()` en init)

### Backup

Para la distribución de `.exe`:
- BD se crea en `%APPDATA%\MiTiendaPoS\` en Windows
- Backup manual: copiar `pos.db` a ubicación segura
- Script backup: Ver `routes.py` endpoint `/api/backup`

---

## 6. Monitoreo & Logs

### Logs Locales

- **App logs**: stdout durante ejecución
- **HTTP logs**: Flask logs en consola
- **Database**: SQLAlchemy echo logs (desactivados por defecto)

**Habilitar SQL debugging**:
```python
# app.py
app.config['SQLALCHEMY_ECHO'] = True
```

### Error Handling

- API endpoints devuelven JSON con `success`, `message`, `data`
- HTTP 400 para validación, 500 para errores server
- Errors logeados en `routes.py` con context

### Future: Structured Logging

Para escalar, migrar a:
- `python-json-logger` para JSON logs
- Enviados a centralized logging (ELK, Datadog, etc.)

---

## 7. Seguridad

### Consideraciones Actuales

- **CORS**: Habilitado para desarrollo (`Flask-CORS`)
- **Auth**: Ninguna (app local de escritorio, trusted network)
- **Secrets**: Base de datos local (no sync a cloud)

### Hardening (Future)

Cuando se exponga a red:
1. Habilitar CSRF protection
2. Agregar autenticación (JWT o sesión)
3. HTTPS en producción
4. Secrets management (environment variables o vault)
5. Input validation & SQL injection prevention (SQLAlchemy ORM ya previene)

---

## 8. Deployment & Release Process

### Workflow Actual

1. **Develop**: Feature branch desde `main`
2. **Test**: Push → GitHub Actions CI pasa
3. **Review**: PR review + merge
4. **Build**: Manual `python build_exe.py` en Windows
5. **Distribute**: GitHub Releases o distribución manual

### Workflow Sugerido (Future)

1. **Automated builds on tag**:
   ```bash
   git tag v1.2.3
   git push --tags
   # → Trigger release workflow
   # → Compile en windows-latest
   # → Publish to GitHub Releases
   ```

2. **Changelog generation**: Auto-generate desde commit messages

3. **Staging environment**: Optional, para QA pre-release

---

## 9. Incident Response

### Common Issues

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| CI fails | Check GitHub Actions logs | Fix tests, push new commit |
| Build fails locally | Missing dependencies | `pip install -r requirements*.txt` |
| DB locked | Multiple app instances | Kill older processes |
| Port 5000 in use | Another app using port | Change in `app.py` or kill process |

### Rollback

Si un release es defectuoso:
1. Revert commit: `git revert <commit>`
2. Push: `git push origin main`
3. Re-build `.exe`
4. Disable release tag o agregar nota de "deprecated"

---

## 10. SRE Responsibilities Checklist

### Weekly
- [ ] Check GitHub Actions failures
- [ ] Review commits para code quality
- [ ] Monitor DB size en distributed instances

### Monthly
- [ ] Dependency updates check (security)
- [ ] Backup integrity test
- [ ] Performance review (si hay logs centralizados)

### Quarterly
- [ ] Upgrade Python version (3.11 → 3.12 cuando sea viable)
- [ ] Dependency bumps (Flask, SQLAlchemy, etc.)
- [ ] Security audit (OWASP top 10)
- [ ] Capacity planning (si hay growth metrics)

---

## 11. Contactos & Documentación

**Repo**: https://github.com/vertexcreations/amara  
**Issues**: GitHub Issues tab  
**Docs**: README.md (user-facing), CLAUDE.md (dev context), este SRE_GUIDE.md (ops)  

**Equipo**:
- **Dev Lead**: Vertex Creations (git config)
- **SRE**: You (this document author)

---

## Apéndice: Útiles Commands

```bash
# Clonar repo
git clone https://github.com/vertexcreations/amara.git
cd amara

# Dev setup
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements-dev.txt

# Test locally
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html  # Generate HTML report

# Build .exe
python build_exe.py

# Check .gitignore
git status  # Should not show .venv, dist, __pycache__, etc.

# View CI logs
# → Open https://github.com/vertexcreations/amara/actions

# Manual tag & release
git tag v1.0.0 -m "Release 1.0.0"
git push --tags

# Revert a commit
git revert <commit-hash>
git push origin main
```

---

**Documento generado**: 2026-06-15  
**Versión**: 1.0  
**Last updated**: 2026-06-15
