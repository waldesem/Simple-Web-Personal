<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useAsyncState } from "@vueuse/core";
import { formUser } from "@/schema/forms";
import { userCols, userDivs } from "@/schema/users";
import { session } from "@/state";
import { Actions, Roles, type User } from "@/types";

// Определяем переменные для работы с данными
const content = ref<"form" | "item">("form");
const modal = ref(false);
const user = ref({} as User);

const { execute, isLoading, state } = useAsyncState<User[]>(
  async () => await ky.get("/routes/users").json(),
  [],
);

// Объявляем функцию для действия с пользователем
async function edit(action: Actions | Roles, userId: string) {
  if (userId === session.value.id) return;
  if (!confirm("Подтвердить действие?")) return;
  const resp = await ky.post("/routes/user/" + userId, {
    json: { actions: action },
  });
  if (resp?.status == 201) {
    await execute();
    alert("Действие успешно выполнено");
  } else alert("Невозможно выполнить действие!");
}

async function submit(form: User) {
  const resp = await ky.post("/routes/user", { json: form });
  if (resp.status === 201) {
    await execute();
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
            icon="i-lucide-user-plus"
            size="lg"
            title="Добавить пользователя"
            variant="ghost"
            @click="
              content = 'form';
              modal = true;
            "
          />
          <template #body>
            <FormDiv
              v-if="content === 'form'"
              :fields="formUser"
              @submit="submit"
            />
            <ItemDiv v-else :item="user" :fields="userDivs">
              <UDropdownMenu :items="actions(user)">
                <UButton
                  color="neutral"
                  icon="i-lucide-chevron-down"
                  label="Действия"
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
            content = 'item';
            modal = true;
            user = row;
          }
        "
      />
    </UPageBody>
  </UContainer>
</template>
