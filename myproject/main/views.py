from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterUserForm, RegisterUserPhotoForm
from django.contrib import messages
from .models import User, UserPhoto, Right, UserRight
import os
import random
from django.conf import settings


class RegisterView(View):
    def get(self, request):
        user_form = RegisterUserForm()
        photo_form = RegisterUserPhotoForm()
        return render(request, 'main/form.html', {
            'user_form': user_form,
            'photo_form': photo_form
        })

    def post(self, request):
        user_form = RegisterUserForm(request.POST)
        photo_form = RegisterUserPhotoForm(request.POST, request.FILES)

        if user_form.is_valid() and photo_form.is_valid():
            # Сохраняем пользователя
            user = user_form.save()
            # Сохраняем фотографию и привязываем ее к пользователю
            photo = photo_form.save(commit=False)
            photo.user = user
            photo.save()

            # Назначаем пользователю стандартные права
            default_right = Right.objects.get(name="Пользователь")
            user_right = UserRight(id_user=user, id_right=default_right, actual_state=True)
            user_right.save()

            messages.success(request, "Пользователь успешно зарегистрирован.")
            return redirect('home')
        else:
            # Если есть ошибки
            messages.error(request, "Ошибка в форме.")
            return render(request, 'main/form.html', {
                'user_form': user_form,
                'photo_form': photo_form
            })


class HomeClass(View):
    def get(self, request):
        cats_folder = os.path.join(settings.BASE_DIR, "main", "static", "main", "img", "cats")

        try:
            cat_images = os.listdir(cats_folder)
            random_cat = random.choice(cat_images) if cat_images else None
        except FileNotFoundError:
            random_cat = None

        return render(request, "main/home.html", {"cat_image": f"main/img/cats/{random_cat}" if random_cat else None})


class UserListClass(View):
    def get(self, request):
        users = User.objects.filter(is_blocked=False, removed=False)
        return render(request, 'main/user_list.html', {'users': users})


class UserDetailClass(View):
    def get(self, request, id):
        # Получаем пользователя по ID
        user = get_object_or_404(User, id=id)

        # Получаем права пользователя
        rights = UserRight.objects.filter(id_user=user)
        rights_list = [right.id_right.name for right in rights]  # Список прав

        # Получаем фотографии пользователя
        photos = UserPhoto.objects.filter(user=user)

        # Передаем все данные в шаблон
        return render(request, 'main/user_detail.html', {
            'user': user,
            'rights': rights_list,
            'photos': photos
        })


class EditRecordClass(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        user_form = RegisterUserForm(instance=user)  # Заполняем форму данными пользователя

        # Получаем первую фотографию пользователя, если она существует
        user_photo = UserPhoto.objects.filter(user=user).first()

        # Если фотография существует, передаем её в форму
        if user_photo:
            photo_form = RegisterUserPhotoForm(instance=user_photo)
        else:
            photo_form = RegisterUserPhotoForm()

        return render(request, 'main/edit_record.html', {
            'user_form': user_form,
            'photo_form': photo_form,
            'user': user
        })

    def post(self, request, id):
        user = get_object_or_404(User, id=id)  # Получаем запись пользователя по ID
        user_form = RegisterUserForm(request.POST, instance=user)

        # Получаем первую фотографию пользователя
        user_photo = UserPhoto.objects.filter(user=user).first()

        # Если фотография существует, обновляем её
        if user_photo:
            photo_form = RegisterUserPhotoForm(request.POST, request.FILES, instance=user_photo)
        else:
            photo_form = RegisterUserPhotoForm(request.POST, request.FILES)

        if user_form.is_valid() and photo_form.is_valid():
            user_form.save()  # Сохраняем изменения пользователя
            photo_form.save()  # Сохраняем изменения фотографии

            messages.success(request, "Запись успешно обновлена.")
            return redirect('users_list')  # Перенаправляем на список пользователей
        else:
            messages.error(request, "Ошибка в форме.")
            return render(request, 'main/edit_record.html', {
                'user_form': user_form,
                'photo_form': photo_form,
                'user': user
            })


class DeleteUserView(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        user.removed = True
        user.save()
        messages.success(request, "Пользователь помечен как удалённый.")
        return redirect('users_list')
