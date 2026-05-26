<script setup lang="ts">
import ky from "ky";
import { computed, ref } from "vue";
import { useAsyncState } from "@vueuse/core";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elements";
import { itemsFields } from "@/schema/items";
import type { Person } from "@/types";

// Определяем данные которые передаются через router из HomePage.vue
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const flag = ref(false);

const { execute, isLoading, state } = useAsyncState<Person>(
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
    <UPageHeader :title="fullname">
      <template #links>
        <UButton
          :color="flag ? 'success' : 'error'"
          :icon="flag ? 'i-lucide-pencil' : 'i-lucide-pencil-off'"
          :title="flag ? 'Откл.Редакт.' : 'Вкл.Редакт.'"
          @click="flag = !flag"
        />
      </template>
    </UPageHeader>

    <UPageBody>
      <UTabs :items="[anketaTab, ...itemsTabs]" :unmount-on-hide="false">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <SkeletDivs v-if="isLoading" :rows="itemsFields.person.length" />
          <PersonView v-else :flag="flag" :person="state" @update="execute" />

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
                :flag="flag"
                :title="accord.label"
                :view="accord.slot"
              />
            </template>
          </UAccordion>
        </template>

        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in itemsTabs" #[tab.slot] :key="tab.slot">
          <ItemView
            :cand-id="props.id"
            :flag="flag"
            :title="tab.label"
            :view="tab.slot"
          />
        </template>
      </UTabs>
    </UPageBody>
  </UContainer>
</template>
