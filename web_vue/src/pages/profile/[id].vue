<script setup lang="ts">
import ky from "ky";
import { shallowRef } from "vue";
import { useAsyncState, useClipboard } from "@vueuse/core";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elems";
import { person as PersonItem } from "@/schema/items";
import { person as PersonForm } from "@/schema/forms";
import type { Person } from "@/types";

definePage({ meta: { layout: "UserLayout" }, props: true });

const props = defineProps({
  id: { type: String, required: true }, // ID кандидата из HomePage.vue
});

const { copy, copied } = useClipboard();

const modal = shallowRef(false); // Объявляем переменную модального окна

const { execute, state, isLoading } = useAsyncState<Person>(
  async () => await ky.get("/api/persons/" + props.id).json(),
  {} as Person,
);

// Определяем функцию для отправки данных формы на сервер
async function submit(form: Person) {
  modal.value = false;
  isLoading.value = true;
  const { status } = await ky.patch("/api/persons/" + props.id, {
    json: form,
  });
  if (status !== 200) alert("Невозможно выполнить действие!");
  await execute();
}
</script>

<template>
  <UContainer>
    <UPageHeader
      :title="`${state.surname} ${state.firstname} ${state.patronymic ?? ''}`"
    />
    <UPageBody>
      <UTabs :items="[anketaTab, ...itemsTabs]" :unmount-on-hide="false">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <ItemDiv
            :class="{ 'animate-pulse': isLoading }"
            :fields="PersonItem"
            :item="state"
            @delete="null"
            @update="modal = true"
          >
            <template #destination>
              <UButton
                v-if="state?.destination"
                :color="copied ? 'success' : 'info'"
                :label="copied ? 'Скопировано' : 'Копировать'"
                size="sm"
                variant="outline"
                @click="copy(state.destination)"
              />
            </template>
          </ItemDiv>

          <!-- Модальное окно для редактирования данных -->
          <UModal
            v-model:open="modal"
            title="Aнкета"
            description="Редактирование анкетные данные"
          >
            <template #body>
              <FormDiv :fields="PersonForm" :item="state" @submit="submit" />
            </template>
          </UModal>

          <USeparator />

          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <UAccordion :items="itemsAccordion">
            <template
              v-for="accord in itemsAccordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ItemView
                :cand-id="props.id"
                :title="accord.label"
                :view="accord.slot"
              />
            </template>
          </UAccordion>
        </template>

        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in itemsTabs" #[tab.slot] :key="tab.slot">
          <ItemView :cand-id="props.id" :title="tab.label" :view="tab.slot" />
        </template>
      </UTabs>
    </UPageBody>
  </UContainer>
</template>
