from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            is_main = form.cleaned_data.get('is_main')
            if is_main:
                count += 1

        if count == 0:
            raise ValidationError('Главный тег должен быть указан!')
        elif count > 1:
            raise ValidationError('Главный тег может быть только один!')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [ 
        'title', 
        'text',
        'published_at',
        ]
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']