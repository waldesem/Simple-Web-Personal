<script setup lang="ts">
import ky from "ky";
import { computed } from "vue";
import { useAsyncState } from "@vueuse/core";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elements";
import type { Person } from "@/types";

// Определяем данные которые передаются через router из HomePage.vue
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const { execute, state } = useAsyncState<Person>(
  async () => await ky.get("/routes/persons/" + props.id).json(),
  {} as Person,
);

const fullname = computed(
  () =>
    `${state.value?.surname ?? ""} ${state.value?.firstname ?? ""} ${
      state.value?.patronymic ?? ""
    }`,
);
</script>

<template>
  <UContainer>
    <UPageHeader :title="fullname" />
    <UPageBody>
      <UTabs :items="[anketaTab, ...itemsTabs]" :unmount-on-hide="false">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <PersonView :person="state" @update="execute" />

          <USeparator />

          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <UAccordion :items="itemsAccordion" :unmount-on-hide="false">
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
