<script setup lang="ts">
import type { Items } from "@/types";

const toast = useToast();

const edit = useEdit();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  data: {
    type: Array as PropType<Items[keyof Items]>,
    default: () => [],
  },
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
});

function capitalize(str: string) {
  if (typeof str == "string") return str.charAt(0).toUpperCase() + str.slice(1);
  else return "";
}

const ItemComponent = defineAsyncComponent<Component>(
  () => import(`../items/${capitalize(props.view)}Item.vue`),
);
const FormComponent = defineAsyncComponent<Component>(
  () => import(`../forms/${capitalize(props.view)}Form.vue`),
);

// Инжектируем данные (id кандидата и доступна ли анкета для редактирования)
const candId = inject("candId") as Ref<string>;

// Объявляем переменные для работы с данными
const data = shallowRef(props.data); // Данные для вывода
const item = shallowRef<object>({}); // Данные для редактирования
const modal = ref(false); // Флаг для открытия модального окна

// Определяем функцию для получения данных из API
async function getItem() {
  data.value = await $fetch(`/routes/${props.view}/${candId.value}`);
}

const fail = () => {
  toast.add({
    title: "Ошибка",
    description: "Невозможно выполнить действие.",
    color: "error",
  });
};

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  const { status } = (await $fetch.raw(
    `/routes/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    },
  ));
  item.value = {};
  await getItem();
  if (status === 201) {
    toast.add({
      title: "Успех",
      description: "Информация успешно обновлена",
      color: "success",
    });
  } else fail();
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { status } = (await $fetch.raw(`/routes/${props.view}/${itemId}`, {
    method: "DELETE",
  }));
  await getItem();
  if (status === 204) {
    toast.add({
      title: "Успех",
      description: "Информация успешно удалена",
      color: "success",
    });
  } else fail();
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty v-if="!data?.length" class="m-4" title="Данные отсутствуют" size="sm">
    <template #body>
      <UButton
        v-if="edit"
        label="Добавить запись"
        variant="outline"
        size="sm"
        @click="modal = true"
      />
    </template>
  </UEmpty>

  <div v-for="(content, index) in data" :key="index" class="mx-2 py-2">
    <!-- Выводим кнопки редактирования/удаления данных, в режиме редактирования -->
    <ElementDivMenu
      v-if="edit"
      @update="
        item = content;
        modal = true;
      "
      @delete="deleteItem(content.id)"
    />
    <!-- Выводим элемент данных -->
    <component :is="ItemComponent" :item="content" />
    <USeparator v-if="index + 1 < data.length" />
  </div>

  <!-- Модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    :title="props.title"
    description="Добавить/редактировать данные"
  >
    <UButton
      v-if="edit && data?.length"
      class="mb-2"
      label="Добавить запись"
      variant="outline"
      size="sm"
      block
    />
    <template #body>
      <component :is="FormComponent" :item="item" @update="submitItem" />
    </template>
  </UModal>
</template>
