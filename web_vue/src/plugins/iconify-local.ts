// File: /plugins/iconify-local.ts

import { addCollection } from "@iconify/vue";
import lucideIcons from "@iconify-json/lucide/icons.json";
import type { IconifyJSON } from "@iconify/types";

// Preload collections
addCollection(lucideIcons as IconifyJSON);

export default {
  install() {
    // Collections already loaded above
  },
};
