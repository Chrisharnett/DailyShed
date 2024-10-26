export const applicationData = {
  title: "DailyShed",
  description: "A Daily Practice Method",
  pages: [
    // HomePage
    {
      title: "Homepage",
      path: "/",
      brand: "DailyShed",
      private: false,
    },
    // The Shed
    {
      title: "The Shed",
      path: "/theShed",
      private: true,
    },
    // User Profile
    {
      title: "Practice Session",
      path: "/userProfile",
      private: true,
    },
    // Practice Journal
    {
      title: "Practice Journal",
      path: "/practiceJournal",
      private: true,
    },
    // Program
    {
      title: "Practice Programs",
      path: "/programs",
      private: true,
    },
    // Contact
    {
      title: "Contact",
      type: "Contact",
      private: false,
      email: "harnettmusic@gmail.com",
      links: [
        //   {
        //     site: "linkedin",
        //     link: "linkedin.com/in/chrisharnettdeveloper",
        //   },
        //   { site: "facebook", link: "" },
        //   { site: "github", link: "https://github.com/Chrisharnett" },
      ],
      path: "/contact",
    },
  ],
  footer: {
    copyright: "&#169; HarnettMusic",
    links: [],
  },
};
