<script setup lang="ts">
import ky from "ky";
import { h, resolveComponent, shallowRef } from "vue";
import { useAsyncState } from "@vueuse/core";
import { TableColumn } from "@nuxt/ui";
import { localStr } from "@/utils";
import { user as formUser } from "@/schema/forms";
import type { Row } from "@tanstack/vue-table";
import { Actions, type User } from "@/types";

definePage({ meta: { layout: "AdminLayout" } });

// Определяем переменные для работы с данными
const globalFilter = shallowRef("");
const method = shallowRef<"POST" | "PATCH">("POST");
const modal = shallowRef(false);
const user = shallowRef({} as User);

const Button = resolveComponent("UButton");
const DropdownMenu = resolveComponent("UDropdownMenu");

// Определяем колонки таблицы
const columns: TableColumn<User>[] = [
  { accessorKey: "id", header: "#" },
  { accessorKey: "fullname", header: "Пользователь" },
  { accessorKey: "username", header: "Логин" },
  { accessorKey: "role", header: "Роль" },
  {
    accessorKey: "created",
    header: "Создан",
    cell: ({ row }) => localStr(row.original.created),
  },
  {
    accessorKey: "attempt",
    header: "Попыток",
    cell: ({ row }) => row.original.attempt,
  },
  {
    accessorKey: "blocked",
    header: "Блокир.",
    cell: ({ row }) => (row.original.blocked ? "Да" : "Нет"),
  },
  {
    accessorKey: "change_pswd",
    header: "Изм.пароль",
    cell: ({ row }) => (row.original.change_pswd ? "Да" : "Нет"),
  },
  {
    accessorKey: "deleted",
    header: "Удален",
    cell: ({ row }) => (row.original.deleted ? "Да" : "Нет"),
  },
  {
    id: "actions",
    meta: {
      class: {
        td: "text-right",
      },
    },
    cell: ({ row }) => {
      return h(
        DropdownMenu,
        {
          content: {
            align: "end",
          },
          items: getRowItems(row),
        },
        () =>
          h(Button, {
            icon: "i-mi-options-vertical",
            color: "neutral",
            variant: "ghost",
          }),
      );
    },
  },
];

// Определяем функцию для получения элементов меню
function getRowItems(row: Row<User>) {
  return [
    {
      label: "Редактировать",
      onSelect() {
        user.value = row.original;
        method.value = "PATCH";
        modal.value = true;
      },
    },
    {
      label: row.original.deleted ? "Восстановить" : "Удалить",
      onSelect() {
        edit(Actions.delete, row.original.id);
      },
    },
    {
      label: row.original.blocked ? "Разблокировать" : "Заблокировать",
      onSelect() {
        edit(Actions.block, row.original.id);
      },
    },
    {
      label: "Сбросить пароль",
      onSelect() {
        edit(Actions.reset, row.original.id);
      },
    },
  ];
}

const { execute, isLoading, state } = useAsyncState<User[]>(
  async () => await ky.get("/api/users/").json(),
  [],
);

async function submit(form: User) {
  modal.value = false;
  const url =
    "/api/users" + (method.value === "POST" ? "/" : "/" + user.value.id);
  const resp = await ky(url, { method: method.value, json: form });
  user.value = {} as User;
  if (resp.status === 201) {
    await execute();
    alert("Пользователь успешно добавлен");
  } else alert("Невозможно выполнить действие!");
}

// Объявляем функцию для действия с пользователем
async function edit(action: Actions, id: string) {
  if (!confirm("Подтвердить действие?")) return;
  const resp = await ky.get("/api/users/" + id, {
    searchParams: { action: action },
  });
  if (resp.status === 200) {
    await execute();
  } else alert("Невозможно выполнить действие!");
}
</script>

<template>
  <UContainer>
    <UPageHeader title="ПОЛЬЗОВАТЕЛИ" :ui="{ title: 'text-2xl text-gray-600' }">
      <template #links>
        <UModal v-model:open="modal" title="Пользователь">
          <UButton
            :loading="isLoading"
            color="neutral"
            icon="i-mi-user-add"
            size="xl"
            title="Добавить пользователя"
            variant="ghost"
            @click="
              method = 'POST';
              modal = true;
            "
          />
          <template #body>
            <FormDiv :fields="formUser" :item="user" @submit="submit" />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <UPageBody>
      <UInput
        id="search"
        icon="i-mi-search"
        v-model.trim="globalFilter"
        :loading="isLoading"
        type="search"
        placeholder="поиск..."
      />
      <UTable
        class="flex-1"
        empty="Нет данных"
        :columns="columns"
        :data="state"
        v-model:global-filter="globalFilter"
        :loading="isLoading"
        loading-animation="swing"
        loading-color="info"
      />
    </UPageBody>
  </UContainer>
</template>
