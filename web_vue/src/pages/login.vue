<script lang="ts">
import type { AuthFormField, FormError, FormSubmitEvent } from '@nuxt/ui';

export interface Auth {
  message: string;
  access_token?: string;
  refresh_token?: string;
}

interface Login {
  username: string;
  password: string;
}

interface Register extends Login {
  new_pswd: string;
  conf_pswd: string;
}

// Login form fields
const login: AuthFormField[] = [
  {
    name: 'username',
    label: 'Имя пользователя',
    icon: 'i-lucide-user',
    type: 'text',
    required: true,
  },
  {
    name: 'password',
    label: 'Пароль',
    icon: 'i-lucide-lock',
    type: 'password',
    required: true,
  },
];

// Update password fields
const register = login.concat([
  {
    name: 'new_pswd',
    label: 'Новый пароль',
    icon: 'i-lucide-lock',
    type: 'password',
    required: true,
  },
  {
    name: 'conf_pswd',
    label: 'Подтверждение пароля',
    icon: 'i-lucide-lock',
    type: 'password',
    required: true,
  },
]);

const auth = {
  post: login,
  patch: register,
};

/*
 * Функция для валидации формы входа/регистрация.
 */
function validateLog(state: Login): FormError[] {
  const errors = [];
  if (!state.username)
    errors.push({ name: 'username', message: 'Обязательное поле!' });
  if (!state.password)
    errors.push({ name: 'password', message: 'Обязательное поле!' });
  return errors;
}

/*
 * Валидация формы обновления пароля пользователя
 */
function validateReg(state: Register): FormError[] {
  const errors = validateLog(state);
  if (!state.new_pswd)
    errors.push({ name: 'new_pswd', message: 'Обязательное поле!' });
  else if (state.password === state.new_pswd)
    errors.push({
      name: 'new_pswd',
      message: 'Новый пароль не должен совпадать с текущим!',
    });
  else if (
    !state.new_pswd.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z0-9]{8,16}$/)
  )
    errors.push({
      name: 'new_pswd',
      message: 'От 8 до 16 символов: заглавные и строчные буквы, цифры',
    });
  if (!state.conf_pswd)
    errors.push({ name: 'conf_pswd', message: 'Обязательное поле!' });
  else if (state.new_pswd !== state.conf_pswd)
    errors.push({
      name: 'conf_pswd',
      message: 'Новый пароль и подтверждение не совпадают!',
    });
  return errors;
}

const validate = {
  post: validateLog,
  patch: validateReg,
};
</script>

<script setup lang="ts">
import ky from 'ky';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/composables';
import { access, refresh } from '@/state';

const router = useRouter();

const { alert, update } = useAlert();

// Объявляем переменные для формы и состояния
const method = ref<'post' | 'patch'>('post');

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Register | Login>) {
  const resp = await ky('auth/login', {
    baseUrl: '/api/',
    method: method.value,
    json: payload.data,
  });
  if (resp.ok) {
    const { message, access_token, refresh_token } =
      (await resp.json()) as Auth;
    if (message === 'success') {
      access.value = access_token;
      refresh.value = refresh_token;
      return router.replace('/');
    } else if (message === 'denied') {
      update('warning', 'Требуется смена пароля.');
      method.value = 'patch';
    } else if (message === 'updated') {
      method.value = 'post';
      update('success', 'Пароль изменен. Войдите с новым паролем.');
    } else update('error', 'Неправильный логин или пароль');
  } else update();
}
</script>

<template>
  <UPageCard class="w-full max-w-md m-auto my-[20vh]">
    <UAuthForm
      icon="i-lucide-lock"
      title="Вход в систему"
      description="Доступ в систему кадровой безопасности."
      :validate="validate[method]"
      :fields="auth[method]"
      :submit="{
        label: method === 'post' ? 'Войти' : 'Изменить',
        color: 'success',
        variant: 'outline',
      }"
      :ui="{ leadingIcon: 'primary' }"
      @submit.prevent="onSubmit($event)"
    >
      <template #validation>
        <UAlert variant="subtle" v-bind="{ ...alert }" />
      </template>
      <template #footer>
        <UButton
          :label="method == 'post' ? 'Изменить' : 'Отмена'"
          color="secondary"
          variant="outline"
          block
          @click="
            () => {
              if (method == 'post') {
                method = 'patch';
                update('info', 'Введите новый пароль и подтверждение.');
              } else {
                method = 'post';
                update('success', 'Введите логин и пароль');
              }
            }
          "
        />
      </template>
    </UAuthForm>
  </UPageCard>
</template>
