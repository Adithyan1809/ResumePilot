from app.core.security import hash_password, verify_password
p = 'Password123'
try:
    h = hash_password(p)
    print('HASH_OK', h[:20])
    print('VERIFY_OK', verify_password(p, h))
except Exception as e:
    print('EXC', type(e), e)
