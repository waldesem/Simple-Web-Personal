import purgeCSSPlugin from "@fullhuman/postcss-purgecss";

let plugins = [];

if (process.env.NODE_ENV === "production") {
  plugins.push(
    purgeCSSPlugin({
      content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
      safelist: [
        /-(leave|enter|appear)(|-(to|from|active))$/,
        /^router-link(|-exact)-active$/,
        /data-v-.*/,
      ],
    }),
  );
}

export default { plugins: plugins };
