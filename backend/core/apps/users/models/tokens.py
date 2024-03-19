from django.db import models

from core.apps.common.models import BaseDateTimeModel
from core.apps.users.entities.tokens import Token as TokenEntity


class IssuedToken(BaseDateTimeModel):
    """Only for refresh tokens."""
    subject = models.ForeignKey(
        to='users.CustomUser',
        related_name='issued_tokens',
        on_delete=models.CASCADE,
    )
    jti = models.CharField(max_length=255)
    is_revoked = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    @classmethod
    def from_entity(cls, refresh_token: TokenEntity) -> 'IssuedToken':
        return cls(
            subject_id=refresh_token.subject_id,
            jti=refresh_token.jti,
            expires_at=refresh_token.expires_at,
        )

    class Meta:
        verbose_name = 'Issued token'
        verbose_name_plural = 'Issued tokens'
