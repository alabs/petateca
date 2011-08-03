from django.forms import ModelForm, TextInput, FileInput
from django.template.loader import render_to_string
from django import forms

from book import models as m

class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("book/popupplus.html", {'field': name})
        return html+popupplus

class MultipleSelectWithPop(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("book/popupplus.html", {'field': name})
        return html+popupplus


class BookLinkForm(ModelForm):
    class Meta:
        model = m.BookLink
        widgets = {
            'url': TextInput(attrs={'size':40}),
        }


class BookForm(ModelForm):
    author = forms.ModelMultipleChoiceField(m.Author.objects, widget=MultipleSelectWithPop)
    category = forms.ModelMultipleChoiceField(m.Category.objects, required=False, widget=MultipleSelectWithPop) 

    class Meta:
        model = m.Book
        exclude = ('slug_name', 'poster')


class ImageBookForm(ModelForm):
    class Meta:
        model = m.ImageBook
        exclude = ('creator','title', 'book', 'is_poster',)
        widgets = {
            'src': FileInput(attrs={'size':'15'}),
        }


#add new category  pop-up
class CategoryForm(forms.ModelForm):
    class Meta:
        model = m.Category
        exclude = ('slug_name',)


#add new author pop-up
class AuthorForm(forms.ModelForm):
    class Meta:
        model = m.Author
        exclude = ('slug_name','book',)
