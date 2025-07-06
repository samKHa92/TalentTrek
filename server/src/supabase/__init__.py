# Supabase package for TalentTrek
# Contains all Supabase-related utilities and configuration

from .supabase import supabase_config
from .supabase_auth import supabase_auth

__all__ = ['supabase_config', 'supabase_auth'] 