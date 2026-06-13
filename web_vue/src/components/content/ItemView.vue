<script setup lang="ts">
import ky from "ky";
import { type PropType, shallowRef } from "vue";
import { useAsyncState } from "@vueuse/core";
import { itemsFields } from "@/schema/items";
import { itemsForms } from "@/schema/forms";
import type { Items } from "@/types";

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  candId: { type: String, required: true },
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
});

const { execute, state, isLoading } = useAsyncState<Items[keyof Items][]>(
  async () => await ky.get(`/api/items/${props.view}/${props.candId}`).json(),
  [],
);

const item = shallowRef({} as Items[keyof Items]);
const method = shallowRef<"POST" | "PATCH">("POST");
const modal = shallowRef(false); // Флаг для открытия модального окна
const visible = shallowRef(false);

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  isLoading.value = true;
  const url = `/api/items/${props.view}/${props.candId}`;
  const { status } = await ky(
    method.value === "POST" ? url : url + "/" + item.value.id,
    {
      method: method.value,
      json: { comparator: props.view, ...form },
    },
  );
  await execute();
  item.value = {} as typeof item.value;
  if (status !== 201 && status !== 200) alert("Невозможно выполнить действие!");
  else if (method.value === "POST") {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string, index: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { status } = await ky.delete(`/api/items/${props.view}/${itemId}`);
  if (status === 204) state.value.splice(index, 1);
  else alert("Невозможно выполнить действие!");
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty v-if="!state.length" size="sm" title="Нет данных" variant="naked">
    <template #body>
      <UButton
        label="Добавить запись"
        size="sm"
        variant="outline"
        @click="
          modal = true;
          method = 'POST';
        "
      />
    </template>
  </UEmpty>

  <div @mouseover="visible = true" @mouseleave="visible = false">
    <div
      v-for="(content, index) in state"
      :key="index"
      :class="{ 'animate-pulse': isLoading }"
    >
      <!-- Выводим элемент данных -->
      <ItemDiv
        :item="content"
        :fields="itemsFields[view]"
        @delete="deleteItem(content.id, index)"
        @update="
          item = content;
          modal = true;
          method = 'PATCH';
        "
      />
      <USeparator v-if="index + 1 < state.length" />
    </div>

    <!-- Модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      :description="
        method === 'POST' ? 'Добавить данные' : 'Редактировать данные'
      "
      :title="props.title"
    >
      <Transition name="fade">
        <UButton
          v-if="state.length && visible"
          block
          class="my-2"
          color="neutral"
          icon="i-mi-add"
          title="Добавить запись"
          size="sm"
          variant="outline"
          @click="method = 'POST'"
        />
      </Transition>
      <template #body>
        <FormDiv :item="item" :fields="itemsForms[view]" @submit="submitItem" />
      </template>
    </UModal>
  </div>
</template>
