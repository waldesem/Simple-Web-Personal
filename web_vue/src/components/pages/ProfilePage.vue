<script setup lang="ts">
import ky from "ky";
import { computed } from "vue";
import { useAsyncState } from "@vueuse/core";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elements";
import type { Anketa, Person } from "@/types";

// Определяем данные которые передаются через router из HomePage.vue
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const { state, isLoading } = useAsyncState(
  async () => await ky.get("/api/candidates/" + props.id).json<Anketa>(),
  {} as Anketa,
);

async function getPerson() {
  isLoading.value = true;
  state.value.person = await ky.get("/api/persons/" + props.id).json<Person>();
  isLoading.value = false;
}

const fullname = computed(
  () =>
    `${state.value.person.surname ?? ""} ${state.value.person.firstname ?? ""} ${
      state.value.person.patronymic ?? ""
    }`,
);
</script>

<template>
  <NUContainer>
    <NUPageHeader :title="fullname" />
    <NUPageBody>
      <NUTabs :items="[anketaTab, ...itemsTabs]" :unmount-on-hide="false">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <PersonView
            :is-loading="isLoading"
            :person="state.person"
            @update="getPerson()"
          />
          <NUSeparator />
          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <NUAccordion :items="itemsAccordion" :unmount-on-hide="false">
            <template
              v-for="accord in itemsAccordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ItemView
                :cand-id="props.id"
                :data="state[accord.slot]"
                :title="accord.label"
                :view="accord.slot"
              />
            </template>
          </NUAccordion>
        </template>
        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in itemsTabs" #[tab.slot] :key="tab.slot">
          <ItemView
            :cand-id="props.id"
            :data="state[tab.slot]"
            :title="tab.label"
            :view="tab.slot"
          />
        </template>
      </NUTabs>
    </NUPageBody>
  </NUContainer>
</template>
