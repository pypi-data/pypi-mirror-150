use super::Item;
use chanoma::Corr;
use pyo3::prelude::*;

#[pyclass]
struct Alphabets {
    #[pyo3(get)]
    items: Vec<Item>,
}

#[pymethods]
impl Alphabets {
    #[new]
    fn new() -> Self {
        Self {
            items: chanoma::characters_set::alphabets::Alphabets::new()
                .items()
                .iter()
                .map(Item::from)
                .collect(),
        }
    }
}

#[pyclass]
struct Digits {
    #[pyo3(get)]
    items: Vec<Item>,
}

#[pymethods]
impl Digits {
    #[new]
    fn new() -> Self {
        Self {
            items: chanoma::characters_set::digits::Digits::new()
                .items()
                .iter()
                .map(Item::from)
                .collect(),
        }
    }
}

#[pyclass]
struct Punctuations {
    #[pyo3(get)]
    items: Vec<Item>,
}

#[pymethods]
impl Punctuations {
    #[new]
    fn new() -> Self {
        Self {
            items: chanoma::characters_set::punctuations::Punctuations::new()
                .items()
                .iter()
                .map(Item::from)
                .collect(),
        }
    }
}

#[pyclass]
struct Kanas {
    #[pyo3(get)]
    items: Vec<Item>,
}

#[pymethods]
impl Kanas {
    #[new]
    fn new() -> Self {
        Self {
            items: chanoma::characters_set::kanas::Kanas::new()
                .items()
                .iter()
                .map(Item::from)
                .collect(),
        }
    }
}

#[pyclass]
struct CjkCompatibilities {
    #[pyo3(get)]
    items: Vec<Item>,
}

#[pymethods]
impl CjkCompatibilities {
    #[new]
    fn new() -> Self {
        Self {
            items: chanoma::characters_set::cjk_compatibilities::CjkCompatibilities::new()
                .items()
                .iter()
                .map(Item::from)
                .collect(),
        }
    }
}

#[pymodule]
pub(crate) fn characters_set(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Alphabets>()?;
    m.add_class::<Digits>()?;
    m.add_class::<Punctuations>()?;
    m.add_class::<Kanas>()?;
    m.add_class::<CjkCompatibilities>()?;

    Ok(())
}
