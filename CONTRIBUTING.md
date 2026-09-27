# Contributing to AetherCMS AI

Thank you for your interest in contributing to AetherCMS AI!

## Development Standards

All code must meet enterprise-grade standards:

- **90%+ test coverage** minimum
- **Zero warnings** (linting, build, runtime)
- **Production-ready security**
- **Complete documentation**
- **TypeScript strict mode** (frontend)
- **Type hints** (Python)

## Development Workflow

1. Create a branch: `git checkout -b feature/your-feature`
2. Implement the feature with tests
3. Run tests: `pytest` (backend) or `npm test` (frontend)
4. Commit with clear message: `git commit -am "Add feature description"`
5. Push to GitHub: `git push origin feature/your-feature`
6. Create Pull Request with:
   - Clear title
   - Description of changes
   - Link to related issues
   - Test results

## Code Style

### Python (Backend)
```bash
black app/
flake8 app/
mypy app/
```

### TypeScript (Frontend)
```bash
npm run lint
npm run type-check
```

## Testing

All new features must include tests:

```bash
# Backend
pytest tests/ --cov=app

# Frontend
npm test

# Mobile
flutter test
```

## Module Development

Each module must include:

1. ✅ Functional specification
2. ✅ Database design
3. ✅ Backend implementation
4. ✅ Frontend implementation
5. ✅ Mobile implementation
6. ✅ API endpoints
7. ✅ AI integration
8. ✅ Security considerations
9. ✅ Tests (90%+ coverage)
10. ✅ Documentation
11. ✅ Performance optimization
12. ✅ Deployment verification

Do not proceed to the next module until the current one is complete, tested, documented, and production-ready.

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, perf, test, chore

Example:
```
feat: Add user authentication module

Implemented JWT-based authentication with:
- Login/register endpoints
- Password hashing with bcrypt
- Session management
- Email verification flow

Fixes: #123
```

## Questions?

- Check `docs/MODULE_1_SYSTEM_ARCHITECTURE.md` for architecture overview
- Review existing modules for patterns
- Open an issue for discussion

Thank you for helping build AetherCMS AI! 🚀
