<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useAsyncState } from "@vueuse/core";
import { formUser } from "@/schema/forms";
import { userCols, userDivs } from "@/schema/users";
import { Actions, Roles, type User, type UserForm } from "@/types";

// Определяем переменные для работы с данными
const item = ref<"form" | "item">("form");
const form = ref({} as UserForm);
const method = ref<"PATCH" | "POST">("POST");
const modal = ref(false);
const user = ref({} as User);

const { execute, isLoading, state } = useAsyncState<User[]>(
  async () => await ky.get("/routes/users").json(),
  [],
);

// Объявляем функцию для действия с пользователем
async function edit(action: Actions | Roles, userId: string) {
  //   if (user_id === session.user?.id) return;
  if (!confirm("Подтвердить действие?")) return;
  const resp = await ky.post("/routes/user/" + userId, {
    json: { actions: action },
  });
  if (resp?.status == 201) {
    await execute();
    alert("Действие успешно выполнено");
  } else alert("Невозможно выполнить действие!");
}

async function submit() {
  const resp = await ky("/routes/user", {
    method: method.value,
    json: form.value,
  });
  if (resp.status === 201) {
    await execute();
    form.value = {} as UserForm;
    alert("Пользователь успешно добавлен");
  } else alert("Невозможно выполнить действие!");
}

function actions(user: User) {
  return [
    {
      label: user.deleted ? "Восстановить" : "Удалить",
      onSelect() {
        edit(Actions.delete, user.id);
      },
    },
    {
      label: user.blocked ? "Разблокировать" : "Заблокировать",
      onSelect() {
        edit(Actions.block, user.id);
      },
    },
    {
      label: "Сбросить пароль",
      onSelect() {
        edit(Actions.reset, user.id);
      },
    },
    {
      label: "Изменить роль",
      children: (Object.keys(Roles.admin) as Array<Roles>).map((element) => {
        return {
          label: element,
          onSelect() {
            edit(element, user.id);
          },
        };
      }),
    },
  ];
}
</script>

<template>
  <UContainer>
    <UPageHeader title="ПОЛЬЗОВАТЕЛИ" :ui="{ title: 'text-gray-600' }">
      <template #links>
        <UModal v-model:open="modal" title="Пользователь">
          <UButton
            variant="ghost"
            icon="i-lucide-user-plus"
            size="lg"
            title="Добавить пользователя"
            @click="
              item = 'form';
              modal = true;
            "
          />
          <!-- Вставляем форму для добавления пользователя -->
          <template #body>
            <FormDiv
              v-if="item === 'form'"
              :fields="formUser"
              @submit="submit"
            />
            <ItemDiv v-else :item="user" :fields="userDivs">
              <UDropdownMenu :items="actions(user)">
                <UButton
                  icon="i-lucide-chevron-down"
                  label="Действия"
                  color="neutral"
                  variant="outline"
                />
              </UDropdownMenu>
            </ItemDiv>
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <UPageBody>
      <TableDiv
        :class="{ 'animate-pulse': isLoading }"
        :cols="userCols"
        :data="state"
        @select="
          (row: User) => {
            item = 'item';
            modal = true;
            user = row;
          }
        "
      />
    </UPageBody>
  </UContainer>
</template>
