<script setup lang="ts">
import ky from "ky";
import { defineAsyncComponent, shallowRef } from "vue";
import { useAsyncState } from "@vueuse/core";
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elements";
import type { Items } from "@/types";

const ViewItem = defineAsyncComponent(
  () => import("@/components/views/ItemView.vue"),
);

// Определяем данные которые передаются через router из HomePage.vue
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const fullname = shallowRef("");

const { state } = useAsyncState(
  async () => await ky.get("/api/items/tables/" + props.id).json<Items>(),
  {} as Items,
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
            :person-id="props.id"
            @listnames="(value: string[]) => (fullname = value.join(' '))"
          />
          <NUSeparator />
          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <NUAccordion :items="itemsAccordion" :unmount-on-hide="false">
            <template
              v-for="accord in itemsAccordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ViewItem
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
          <ViewItem
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
